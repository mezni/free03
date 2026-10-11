# Day 16 — Automated Quality Gates

## Objective

Make quality enforcement automatic and reproducible: add a GitHub Actions workflow that runs formatting, linting, and the test suite with coverage on every push and pull request, and configure Ruff, pytest, and coverage so the same checks can be run locally.

## What I created

### `pyproject.toml` configuration

- Added a `dev` optional-dependency group: `ruff`, `pytest`, `pytest-cov`, `httpx`.
- Added `[tool.ruff]`: `line-length = 88`, `target-version = "py311"`.
- Added `[tool.ruff.lint]`: `select = ["E", "F", "I", "UP"]`, `ignore = []`.
- Added `[tool.pytest.ini_options]`: `testpaths = ["tests"]`, `addopts = "-ra"`.
- Added `[tool.coverage.run]`: `source = ["ticket_triage"]`.
- Added `[tool.coverage.report]`: `fail_under = 60`.

I also raised `requires-python` from `>=3.10` to `>=3.11`. The configured `target-version = "py311"` and the Ruff modernization fixes below (`StrEnum`, `datetime.UTC`) require Python 3.11, so the previous `>=3.10` declaration was no longer accurate. CI and Ruff now agree on 3.11.

### `.github/workflows/ci.yml`

Triggered on `push`, `pull_request`, and `workflow_dispatch`, with `contents: read` permissions and a concurrency group that cancels superseded runs. On `ubuntu-latest` with Python 3.11:

1. `python -m pip install -e ".[dev]"`
2. `ruff format --check .`
3. `ruff check .`
4. `pytest --cov=ticket_triage --cov-report=term-missing --cov-fail-under=60`

## Formatting and lint fixes

The gates surfaced pre-existing issues, which I fixed so the checks pass:

- `ruff format .` reformatted 25 files.
- `ruff check --fix .` auto-fixed 19 issues (unused imports `F401`, unsorted imports `I001`).
- `ruff check --fix --unsafe-fixes .` fixed 4 `UP042` findings, converting `class Priority(str, Enum)` (and `CaseStatus`, `DecisionType`, `RoutingStatus`) to `StrEnum`, and modernizing `timezone.utc` to `datetime.UTC` and `"..."`-concatenations.
- One notable side effect: `application.py` imported `record_decision` from the (still missing) `ticket_triage.approval` module but never used it; Ruff removed the dead import.

## Concepts learned

- A quality gate is only useful if it fails the build automatically; a check that a human must remember to run is a suggestion, not a gate.
- CI must pin the same toolchain and Python version used locally, otherwise "passes locally, fails in CI" differences creep in.
- `ruff format --check` and `ruff check` enforce two different things: syntax-level formatting versus lint rules. Both must pass.
- `--cov-fail-under` turns coverage into a ratchet: the suite cannot regress below the threshold, but the threshold should be raised deliberately as the codebase matures, never lowered silently.
- Formatting/lint auto-fixes can touch code you did not write; they belong in their own, clearly-scoped commit so the change is reviewable.

## Testing

Local runs (from the repository root, using the project virtualenv):

```text
$ ruff format --check .
70 files already formatted

$ ruff check .
All checks passed!

$ pytest -q
ERROR tests/integration/test_ticket_lifecycle.py
ERROR tests/test_api.py
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
4 errors in 4.64s
```

Coverage gate:

```text
$ pytest --cov=ticket_triage --cov-report=term-missing --cov-fail-under=60
ERROR tests/integration/test_ticket_lifecycle.py
ERROR tests/test_api.py
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The individual suites that can be imported still pass (29 tests): `test_config`, `test_auth`, `test_openai_client`, `test_llm_classifier`, `test_observability`, `test_evaluation`, `test_resilience`.

The four collection errors are the pre-existing gaps recorded on Days 6–7 and repeated on Day 15:

- `tests/test_domain.py` → `ImportError: cannot import name 'validate_ticket'`.
- `tests/test_workflow.py` → `ImportError: cannot import name 'transition_case'`.
- `tests/test_api.py` → now fails on `transition_case` (via `application.py`); it previously failed on the missing `ticket_triage.approval` module.
- `tests/integration/test_ticket_lifecycle.py` → `ModuleNotFoundError: No module named 'ticket_triage.sqlite_repository'` (via `application.py`'s `approval` import was removed, exposing the next missing dependency).

Because pytest aborts during collection, no coverage report is produced and the `--cov-fail-under=60` threshold is not evaluated. **The CI workflow, as written, will fail at the test step until the missing infrastructure is implemented.** This is recorded honestly rather than worked around.

## Limitations

- The CI test/coverage steps cannot pass yet: the suite does not collect because of the missing `validate_ticket`, `transition_case`, `ticket_triage.approval`, and `ticket_triage.sqlite_repository` pieces.
- The 60% coverage threshold could not be measured because collection aborts before a report is emitted.
- The workflow is validated only by inspection; it has not run on GitHub Actions.
- `ruff format .` and the lint auto-fixes touched several files written on earlier days, so this commit is larger than a typical Day-16 change.

## Validation checklist

- [x] `pyproject.toml` defines Ruff, pytest, and coverage configuration.
- [x] `dev` optional-dependency group added and installed.
- [x] `.github/workflows/ci.yml` added (checkout v4, Python 3.11, format/lint/test gates).
- [x] `ruff format --check .` passes locally.
- [x] `ruff check .` passes locally.
- [ ] Full `pytest` suite passes (blocked by four collection errors).
- [ ] `pytest --cov ... --cov-fail-under=60` passes (blocked; no report produced).
- [x] `docs/progress/day-16.md` written.

## Reflection

- **Why run the same commands in CI and locally?** So that a change that passes on a developer's machine is the same check the build enforces; otherwise CI becomes a surprise gate and trust in it erodes.
- **Why is a failing gate better than a warning?** Warnings are ignored under deadline pressure; a red build blocks the merge and forces the gap to be addressed or explicitly waived.
- **Why does the coverage threshold not help yet?** Coverage measures executed lines; when the suite cannot even be collected there is nothing to measure, so the threshold is inert. It becomes meaningful only after the missing infrastructure lands.

## Next

Implement the missing infrastructure (`sqlite_repository.py`, `approval.py`, `validate_ticket`, `transition_case`, and the remaining `TriageApplicationService` methods) so the full suite collects and the coverage gate can actually be evaluated.

## Day 16 completion checklist

- [x] Add dev dependencies and tool configuration to `pyproject.toml`
- [x] Create `.github/workflows/ci.yml`
- [x] Run `ruff format --check .` (passes)
- [x] Run `ruff check .` (passes)
- [ ] Run `pytest --cov=ticket_triage --cov-report=term-missing --cov-fail-under=60` (recorded; blocked)
- [x] Write `docs/progress/day-16.md`
- [x] Commit with message `ci: add automated quality gates`
- [ ] Push to `origin/main` (pending)
