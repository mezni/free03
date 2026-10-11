# Day 24 — Durable Routing, Idempotency, and Reconciliation

## Objective

Design a recoverable routing workflow that handles retries, timeouts, and
uncertain external outcomes without blindly duplicating side effects.

The central lesson: a timeout means the outcome is *unknown*, not that the
operation failed. The external system may have committed the change even though
the response never reached the application.

## Implementation

- Created a `routing_operations` migration (`migrations.py`) with a foreign key
  to `triage_cases` and a unique `idempotency_key`.
- Added a stable idempotency-key function (`idempotency.routing_idempotency_key`).
- Defined a vendor-neutral provider interface (`routing_provider.RoutingProvider`)
  plus conservative outcome classification.
- Extended `RoutingOperation` with `recommendation_version`, `ticket_id`,
  `destination`, `external_reference`, and `last_error_code`.
- Implemented `SQLiteRoutingOperationRepository` (persisted intent, intent
  discovery on restart, and explicit status transitions).
- Implemented `RoutingService` to persist intent before external calls and to
  record confirmed success, confirmed failure, or unknown outcome.
- Implemented `RoutingReconciler` to resolve unresolved operations against the
  provider before any retry.
- Ensured case completion requires confirmed routing success.

## Task A — Persist routing operations

```sql
CREATE TABLE IF NOT EXISTS routing_operations (
    operation_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    approval_decision_id TEXT NOT NULL,
    recommendation_version INTEGER NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    ticket_id TEXT NOT NULL,
    destination TEXT NOT NULL,
    status TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    external_reference TEXT,
    last_error_code TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES triage_cases (case_id)
);
```

- The schema is applied by `migrations.apply_routing_operations_schema`, an
  additive, idempotent migration re-applied on every adapter startup.
- `SQLiteCaseRepository` and `SQLiteRoutingOperationRepository` both open
  connections with `PRAGMA foreign_keys = ON`; the routing table's foreign key
  is enforced.
- `last_error_code` stores only the exception *type* (`_error_code`), never raw
  messages, credentials, ticket content, or provider response bodies.
- `list_unresolved()` returns `pending`, `in_progress`, `outcome_unknown`, and
  `reconciliation_required` operations — the recovery set discovered after a
  restart.

## Task B — Stable idempotency keys

`routing_idempotency_key(case_id, recommendation_version)` hashes
`ticket-triage:routing:<case_id>:v<version>`. Identical inputs produce the same
key, so retries reuse it; a new recommendation version produces a new key
because it is a different intended effect. Empty case IDs and non-positive
versions are rejected. In a multi-tenant deployment the tenant identifier must
be folded into this identity.

The key is persisted with a `UNIQUE` constraint. That prevents *local*
duplicates but not duplicates at the provider; provider-side idempotency or
reconciliation is still required.

## Task C — Provider interface and outcome categories

```python
class RoutingProvider(Protocol):
    def route(self, *, ticket_id, destination, idempotency_key) -> str: ...
    def lookup_by_idempotency_key(self, idempotency_key) -> str | None: ...
```

- `route` returns a confirmed external reference or raises.
- `lookup_by_idempotency_key` returns a reference when found, `None` only when
  the provider *definitively* confirms absence, and raises
  `RoutingLookupInconclusiveError` when the outcome cannot be determined (for
  example under eventual consistency).
- `RoutingOutcome` distinguishes `CONFIRMED_SUCCESS`, `CONFIRMED_FAILURE`, and
  `UNKNOWN`.
- `classify_provider_error` only treats `RoutingConfirmedFailure` as a
  confirmed failure. Timeouts, connection loss, and unexpected errors are
  classified as `UNKNOWN`, because the side effect may already exist.

## Task D — Safe execution sequence

`RoutingService.request_routing` runs steps 1–4: it verifies approval, computes
the stable key, creates or retrieves the operation, and commits the intent and
the case transition to `ROUTING` *before* any network call.
`RoutingService.execute` runs steps 5–7: it marks the operation in progress,
calls the provider **outside** any database transaction, then persists success,
failure, or unknown. The case is moved to `COMPLETED` only after confirmed
success.

If persisting success fails after the provider committed the action, the
operation never reaches `SUCCEEDED`; it remains in the unresolved set and is
found by reconciliation on restart rather than resent blindly.

## Task E — Reconciliation

`RoutingReconciler.reconcile` decides based on the provider lookup:

| Lookup result | Action |
| --- | --- |
| Found and success confirmed | Persist success and external reference |
| Definitively absent | Retry only when the provider sets `supports_safe_retry` |
| Inconclusive | Keep unresolved (`reconciliation_required`), retry later |
| Confirmed failure | Persist failure and apply the recovery policy |

`supports_safe_retry` defaults to `False`: without an explicit provider
guarantee, an absent lookup leaves the operation unresolved instead of
resending it. An inconclusive lookup never triggers a retry.

## Tests

`tests/test_idempotency.py` (5 tests) and `tests/test_routing_recovery.py`
(11 tests):

- Routing intent is persisted before the provider is called.
- Repeating the same request reuses the existing operation and key (one row).
- A timeout results in `outcome_unknown`, not confirmed failure.
- A provider-confirmed operation is reconciled to `succeeded`.
- An inconclusive lookup does not trigger a blind retry.
- An absent lookup retries only when the provider guarantees safe retries.
- A confirmed failure is persisted and the case is not completed.
- A case is not marked completed while routing remains unresolved.
- A process restart recovers pending and unknown operations from the database.
- Routing is rejected when the approval is missing or stale.
- Existing regression tests continue to pass.

Tests assert persisted state after reopening the repositories, not only the
in-memory objects.

Result: `83 passed` (67 pre-existing + 16 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 93 files already formatted
pytest --cov=ticket_triage ...       -> 84% total coverage (60% gate met)
```

## Architecture Decisions

- **Durability:** routing operations live in the database; an in-memory object
  would be lost on a crash between send and confirm.
- **Idempotency:** one stable key identifies one intended routing effect.
- **Failure handling:** uncertain outcomes are persisted explicitly as
  `outcome_unknown` / `reconciliation_required`, never as failure.
- **Reconciliation:** external state is checked before an uncertain operation is
  retried, and retries require an explicit provider guarantee.
- **Transaction boundaries:** database transactions are short; network calls run
  outside write transactions.
- **Separate lifecycles:** the routing operation and the case progress
  independently; only confirmed success completes the case.

## Remaining Risks

- Idempotency depends on the provider's capabilities and contract; a local key
  alone does not guarantee exactly-once execution.
- Eventual consistency can make immediate reconciliation inconclusive.
- Database failures after external success require recovery via reconciliation.
- Operational monitoring and manual reconciliation procedures are still needed
  for operations that never resolve automatically.

## Lessons Learned

- Network timeouts do not prove external failure.
- Persisting intent before the external call enables recovery after crashes.
- Resending an unresolved operation without checking provider state can
  duplicate side effects.
- A case must not be marked complete without evidence of success.

## Exit Criteria

Routing intent and outcomes are durable, unresolved operations are recoverable
after a restart, and tests demonstrate safe behavior during uncertain provider
outcomes. All quality gates pass.
