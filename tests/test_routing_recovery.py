"""Durable routing, idempotency, and reconciliation regression tests.

These tests assert persisted state by reopening the repositories, not just the
in-memory objects, because the whole point of the day is surviving restarts.
"""

import sqlite3

import pytest

from tests.fakes import FakeRoutingProvider
from ticket_triage.application import TriageApplicationService
from ticket_triage.approval import StaleRecommendationError
from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import (
    CaseStatus,
    DecisionType,
    RoutingStatus,
    Ticket,
)
from ticket_triage.errors import (
    InvalidCaseStateError,
    RoutingConfirmedFailure,
)
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.routing import RoutingService
from ticket_triage.sqlite_repository import (
    SQLiteCaseRepository,
    SQLiteRoutingOperationRepository,
)

POLICY = RecommendationPolicy(
    allowed_categories={"billing", "account", "general"},
    allowed_destinations={
        "billing-team",
        "account-support",
        "general-support",
    },
)


def make_ticket(ticket_id: str = "ticket-1") -> Ticket:
    return Ticket(
        ticket_id=ticket_id,
        subject="Charged twice",
        description="I was charged twice for one order.",
    )


def make_approved_case(
    service: RoutingService,
    case_id: str = "case-1",
) -> str:
    app = TriageApplicationService(service.case_repository)
    app.create_case(case_id=case_id, ticket=make_ticket(f"ticket-{case_id}"))
    app.start_processing(case_id)
    app.classify_case(case_id, classifier=FakeClassifier(), policy=POLICY)
    app.decide(
        case_id,
        decision_id=f"decision-{case_id}",
        actor_id="reviewer-1",
        decision=DecisionType.APPROVED,
    )
    return case_id


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "routing.db")


@pytest.fixture
def case_repository(db_path):
    repository = SQLiteCaseRepository(db_path)
    yield repository
    repository.close()


@pytest.fixture
def routing_repository(db_path):
    repository = SQLiteRoutingOperationRepository(db_path)
    yield repository
    repository.close()


@pytest.fixture
def provider():
    return FakeRoutingProvider()


@pytest.fixture
def service(case_repository, routing_repository, provider):
    return RoutingService(
        case_repository=case_repository,
        routing_repository=routing_repository,
        provider=provider,
    )


def reopen_operations(db_path):
    return SQLiteRoutingOperationRepository(db_path)


def test_intent_is_persisted_before_provider_call(service, case_repository, provider):
    case_id = make_approved_case(service)

    operation = service.request_routing(case_id)

    assert operation.status is RoutingStatus.PENDING
    assert provider.route_calls == []

    # The intent is durable, not just an in-memory object.
    reopened = reopen_operations(service.routing_repository.database_path)
    try:
        stored = reopened.get(operation.operation_id)
    finally:
        reopened.close()
    assert stored is not None
    assert stored.status is RoutingStatus.PENDING
    assert stored.idempotency_key == operation.idempotency_key

    record = case_repository.get_with_revision(case_id)
    assert record is not None
    assert record.case.status is CaseStatus.ROUTING


def test_repeated_request_reuses_operation_and_key(
    service, routing_repository, provider
):
    case_id = make_approved_case(service)

    first = service.request_routing(case_id)
    second = service.request_routing(case_id)

    assert first.operation_id == second.operation_id
    assert first.idempotency_key == second.idempotency_key
    assert provider.route_calls == []

    with sqlite3.connect(routing_repository.database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM routing_operations"
        ).fetchone()[0]
    assert count == 1


def test_timeout_is_unknown_not_confirmed_failure(service, provider):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.accept_then_timeout(operation.idempotency_key)

    result = service.execute(operation.operation_id)

    assert result.status is RoutingStatus.OUTCOME_UNKNOWN
    assert result.status is not RoutingStatus.FAILED
    assert result.last_error_code == "TimeoutError"

    reopened = reopen_operations(service.routing_repository.database_path)
    try:
        stored = reopened.get(operation.operation_id)
    finally:
        reopened.close()
    assert stored.status is RoutingStatus.OUTCOME_UNKNOWN


def test_confirmed_operation_is_reconciled_to_succeeded(
    service, case_repository, provider
):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.accept_then_timeout(operation.idempotency_key)
    assert service.execute(operation.operation_id).status is (
        RoutingStatus.OUTCOME_UNKNOWN
    )

    reconciled = service.reconcile_operation(operation.operation_id)

    assert reconciled.status is RoutingStatus.SUCCEEDED
    assert reconciled.external_reference is not None

    record = case_repository.get_with_revision(case_id)
    assert record.case.status is CaseStatus.COMPLETED


def test_inconclusive_lookup_does_not_trigger_blind_retry(service, provider):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.accept_then_timeout(operation.idempotency_key)
    service.execute(operation.operation_id)
    provider.mark_inconclusive(operation.idempotency_key)
    calls_before = list(provider.route_calls)

    result = service.reconcile_operation(operation.operation_id)

    assert result.status is RoutingStatus.RECONCILIATION_REQUIRED
    assert provider.route_calls == calls_before


def test_absent_lookup_retries_only_when_safe(service, provider):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.fail_route(operation.idempotency_key, TimeoutError("lost"))
    service.execute(operation.operation_id)
    calls_before = list(provider.route_calls)

    # No provider guarantee: keep the operation unresolved instead of resending.
    unresolved = service.reconcile_operation(operation.operation_id)
    assert unresolved.status is RoutingStatus.RECONCILIATION_REQUIRED
    assert provider.route_calls == calls_before

    # With an explicit safe-retry guarantee, the same key is resent and resolves.
    provider.supports_safe_retry = True
    resolved = service.reconcile_operation(operation.operation_id)
    assert resolved.status is RoutingStatus.SUCCEEDED
    assert len(provider.route_calls) == len(calls_before) + 1


def test_case_is_not_completed_while_routing_unresolved(
    service, case_repository, provider
):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.accept_then_timeout(operation.idempotency_key)

    service.execute(operation.operation_id)

    record = case_repository.get_with_revision(case_id)
    assert record.case.status is CaseStatus.ROUTING
    assert record.case.status is not CaseStatus.COMPLETED


def test_confirmed_failure_is_persisted(service, provider):
    case_id = make_approved_case(service)
    operation = service.request_routing(case_id)
    provider.fail_route(
        operation.idempotency_key,
        RoutingConfirmedFailure("The provider rejected the assignment."),
    )

    result = service.execute(operation.operation_id)

    assert result.status is RoutingStatus.FAILED
    assert result.last_error_code == "RoutingConfirmedFailure"


def test_restart_recovers_unresolved_operations(service, db_path, provider):
    pending_case = make_approved_case(service, "case-restart-pending")
    pending = service.request_routing(pending_case)

    unknown_case = make_approved_case(service, "case-restart-unknown")
    unknown = service.request_routing(unknown_case)
    provider.accept_then_timeout(unknown.idempotency_key)
    service.execute(unknown.operation_id)

    # Simulate a process restart: drop every connection and reopen the file.
    service.routing_repository.close()
    service.case_repository.close()

    recovered = reopen_operations(db_path)
    try:
        unresolved = {op.operation_id for op in recovered.list_unresolved()}
        assert pending.operation_id in unresolved
        assert unknown.operation_id in unresolved
    finally:
        recovered.close()


def test_missing_approval_blocks_routing(service):
    app = TriageApplicationService(service.case_repository)
    app.create_case(case_id="case-unapproved", ticket=make_ticket("ticket-u"))
    app.start_processing("case-unapproved")
    app.classify_case(
        "case-unapproved",
        classifier=FakeClassifier(),
        policy=POLICY,
    )

    with pytest.raises(InvalidCaseStateError):
        service.request_routing("case-unapproved")

    with sqlite3.connect(service.routing_repository.database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM routing_operations"
        ).fetchone()[0]
    assert count == 0


def test_stale_approval_blocks_routing(service, case_repository):
    case_id = make_approved_case(service)

    # A newer recommendation version invalidates the earlier approval.
    record = case_repository.get_with_revision(case_id)
    record.case.recommendation_version += 1
    case_repository.save_if_revision(
        record.case,
        expected_revision=record.revision,
    )

    with pytest.raises(StaleRecommendationError):
        service.request_routing(case_id)
