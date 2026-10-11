# Day 23 — Database Transactions and Concurrency Control

## Objective

Prevent duplicate case creation, stale updates, and conflicting approval
decisions using database-enforced guarantees rather than Python timing.

## Prerequisite: built the missing infrastructure

Days 15–22 had been running against a partially missing core. Because Day 23
requires a concrete persistence adapter, this day also implemented the pieces
that had been flagged as missing:

- `domain.validate_ticket()` — returns a list of validation errors.
- `workflow.transition_case()` — applies `ALLOWED_TRANSITIONS` and leaves the
  case untouched on an illegal transition.
- `ticket_triage.approval` — `record_decision()` and `authorize_routing()` plus
  `StaleRecommendationError`.
- `SQLiteCaseRepository` — the persistence adapter (this day's main deliverable).
- `TriageApplicationService` — completed `create_case`, and added `get_case`,
  `start_processing`, `decide`, all using compare-and-swap.

As a result the full test suite now collects and runs (previously 4 collection
errors).

## Concepts Learned

- Transactions and atomicity
- Database uniqueness constraints
- Optimistic concurrency control
- Compare-and-swap updates
- Durable idempotency
- SQLite write-locking behavior

## Implementation

### Task A — Unique case IDs

- Table definition enforces the constraint:

  ```sql
  CREATE TABLE IF NOT EXISTS triage_cases (
      case_id TEXT PRIMARY KEY,
      revision INTEGER NOT NULL DEFAULT 0,
      payload TEXT NOT NULL
  );
  ```

- `SQLiteCaseRepository.create()` uses a plain `INSERT`. A duplicate raises
  `sqlite3.IntegrityError`, which is mapped to `DuplicateCaseError` only when
  the message contains `UNIQUE constraint failed` or `PRIMARY KEY`; other
  integrity failures propagate unchanged.

### Task B — Optimistic concurrency (compare-and-swap)

- Added a database-managed `revision` column (distinct from
  `recommendation_version`).
- `get_with_revision()` returns a `CaseRecord(case, revision)`.
- `save_if_revision(case, expected_revision)` runs:

  ```sql
  UPDATE triage_cases
  SET payload = ?,
      revision = revision + 1
  WHERE case_id = ?
    AND revision = ?;
  ```

  and raises `ConcurrentUpdateError` when `cursor.rowcount != 1`.
- `ConcurrentUpdateError` is a typed error in `errors.py`, mapped to HTTP
  `409 Conflict` in `api.py` (alongside `DuplicateCaseError` and
  `InvalidCaseStateError`).
- The application service reads with `get_with_revision()` and writes with
  `save_if_revision()` for every workflow update, so no unconditional save can
  bypass the guard.

### Task C — Atomic approval persistence

- `approval.record_decision()` enforces the invariant in memory: the case must
  be `PENDING_APPROVAL`, the approval records the current
  `recommendation_version`, and the case transitions in the same step.
- The service persists the resulting payload with a single conditional `UPDATE`,
  so the decision and the new case state commit together in one statement.
- Idempotency: replaying the same `decision_id` returns the previously recorded
  decision without changing the case. A different `decision_id` against an
  already-decided case raises `InvalidCaseStateError` (HTTP 409).
- Approval data remains inside the case payload. The optional append-only
  `approval_decisions` table from the brief is documented as a future schema
  rather than implemented now.

### Schema migration

- New databases get the `revision` column via `CREATE TABLE`.
- For existing databases, `_migrate_revision_column()` inspects
  `PRAGMA table_info(triage_cases)` and runs
  `ALTER TABLE triage_cases ADD COLUMN revision INTEGER NOT NULL DEFAULT 0`
  when the column is absent. `CREATE TABLE IF NOT EXISTS` alone would not add it.
- Migration is applied at adapter construction, before any reads or writes.

## Tests

`tests/test_concurrency.py` (7 tests) plus the now-runnable existing suites:

- Duplicate case creation is rejected (`DuplicateCaseError`).
- A stale revision cannot overwrite newer state (`ConcurrentUpdateError`).
- Conflicting approvals cannot both commit.
- A stale recommendation version cannot authorize routing.
- A failed update leaves no partial approval in storage.
- A repeated `decision_id` is idempotent; a new one conflicts.
- A legacy (pre-revision) database is migrated and readable.

Result: `67 passed`.

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 82 files already formatted
pytest --cov=ticket_triage ...       -> 67 passed
coverage                             -> ~64% api.py / 78% application.py,
                                        ~86% sqlite_repository.py, 60% gate met
```

## Design Notes

The case revision protects persistence against stale writes. The recommendation
version identifies the classification under review. These are separate
concurrency and business-integrity controls: a reviewer can hold the right
recommendation version while acting on stale case state, and vice versa.

Errors are typed (`DuplicateCaseError`, `ConcurrentUpdateError`,
`InvalidCaseStateError`, `CaseNotFoundError`) and mapped to HTTP status codes in
the API layer.

## Migration and recovery assumptions

- The only applied migration is additive (`revision` with a non-null default),
  so it is safe on an existing table and does not rewrite rows.
- No down-migration is provided; rolling back the code while leaving the
  `revision` column in place is harmless for the previous version.
- If a migration is interrupted, the `ALTER TABLE` either committed or not; the
  next startup re-checks the column list and retries, so the operation is
  idempotent.
- `save_if_revision` losing a race is a recoverable condition: reload and retry,
  or surface `409` so the client reloads.

## Limitations

- Cross-process concurrency still requires database-enforced coordination; the
  `revision` check is authoritative but clients must handle `409` and retry.
- SQLite may be unsuitable for a future high-write, multi-instance deployment
  (single-writer locking; WAL helps readers but not write throughput).
- External routing idempotency requires provider cooperation or reconciliation;
  it is not implemented here.
- `authorize_routing()` exists and is unit-tested but is not yet wired to a
  routing endpoint or `RoutingOperation` persistence.
- Repository connections are not explicitly closed (ResourceWarnings appear in
  the test output); a connection lifecycle/pooling strategy is future work.
- The optional append-only `approval_decisions` table and SQLite foreign-key
  enforcement for it are not implemented.

## Lessons Learned

- A read followed by a write is not automatically atomic.
- Database constraints are essential for race-prone invariants.
- Approval records and case transitions must commit together.
- Network operations should not run inside database write transactions.
- Turning on the previously-blocked tests immediately surfaced two stale test
  assumptions (a positional `create_app` call and body-validation ordering),
  which were corrected.

## Exit Criteria

Stale writes are rejected (`ConcurrentUpdateError` → 409), conflicting decisions
cannot both commit, duplicate creates are rejected by the primary key, and each
guarantee is covered by regression tests. All quality gates pass.
