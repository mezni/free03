from ticket_triage.application import TriageApplicationService
from ticket_triage.classification import FakeClassifier
from ticket_triage.classification_worker import handle_classification_job
from ticket_triage.domain import CaseStatus, Ticket
from ticket_triage.job_queue import Job
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.sqlite_repository import SQLiteCaseRepository


def make_dependencies(tmp_path):
    service = TriageApplicationService(
        SQLiteCaseRepository(str(tmp_path / "worker-test.db"))
    )
    classifier = FakeClassifier()
    policy = RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )
    ticket = Ticket(
        ticket_id="T-100",
        subject="Charged twice",
        description="I see two charges on my account.",
    )
    return service, classifier, policy, ticket


def classify_job(attempts: int = 1) -> Job:
    return Job(
        job_id="classify:case-001",
        job_type="classify_ticket",
        payload={"case_id": "case-001"},
        status="running",
        attempts=attempts,
    )


def test_worker_classifies_case_and_stops_at_approval(tmp_path):
    service, classifier, policy, ticket = make_dependencies(tmp_path)
    service.create_case(case_id="case-001", ticket=ticket)

    handle_classification_job(
        classify_job(),
        service=service,
        classifier=classifier,
        policy=policy,
    )

    case = service.get_case("case-001")
    assert case.status == CaseStatus.PENDING_APPROVAL
    assert case.recommendation is not None


def test_retried_job_does_not_reclassify_completed_work(tmp_path):
    service, classifier, policy, ticket = make_dependencies(tmp_path)
    service.create_case(case_id="case-001", ticket=ticket)
    service.start_processing("case-001")
    service.classify_case("case-001", classifier=classifier, policy=policy)

    original = service.get_case("case-001").recommendation

    handle_classification_job(
        classify_job(attempts=2),
        service=service,
        classifier=classifier,
        policy=policy,
    )

    case = service.get_case("case-001")
    assert case.status == CaseStatus.PENDING_APPROVAL
    assert case.recommendation == original
    assert case.recommendation_version == 1


def test_worker_rejects_unsupported_job_type(tmp_path):
    service, classifier, policy, ticket = make_dependencies(tmp_path)
    service.create_case(case_id="case-001", ticket=ticket)

    job = Job(
        job_id="route:case-001",
        job_type="route_ticket",
        payload={"case_id": "case-001"},
        status="running",
        attempts=1,
    )

    try:
        handle_classification_job(
            job,
            service=service,
            classifier=classifier,
            policy=policy,
        )
    except ValueError as exc:
        assert "Unsupported job type" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected an unsupported job type to be rejected.")


def test_worker_requires_case_id_in_payload(tmp_path):
    service, classifier, policy, ticket = make_dependencies(tmp_path)

    job = Job(
        job_id="classify:missing",
        job_type="classify_ticket",
        payload={},
        status="running",
        attempts=1,
    )

    try:
        handle_classification_job(
            job,
            service=service,
            classifier=classifier,
            policy=policy,
        )
    except ValueError as exc:
        assert "case_id" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected a missing case_id to be rejected.")
