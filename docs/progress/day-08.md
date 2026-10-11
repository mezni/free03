# Day 8 — Structured LLM Output

## Objective

Create a provider-neutral LLM adapter that converts raw model responses into domain recommendations.

## Implemented

- Defined the `LLMClient` protocol.
- Implemented `LLMClassifier`.
- Added JSON parsing and schema validation.
- Rejected missing fields, unexpected fields, incorrect types, and invalid priorities.
- Stripped Markdown code fences from responses.
- Rejected empty required fields.
- Wrapped provider/client failures in `ClassificationError`.
- Added a fake LLM client for deterministic tests.
- Tested valid and malformed responses.

## Architecture concepts

### Adapter pattern

The LLM adapter translates a provider's response into the application's domain model (`src/ticket_triage/llm_classifier.py`).

### Contract validation

Parsing JSON proves only that the response is syntactically valid. Schema and policy validation enforce additional constraints.

### Separation of concerns

The LLM proposes. The adapter parses. The policy validates permitted values. The application coordinates the workflow. A human approves.

Prompt instructions treat ticket content as untrusted, but a prompt alone is not a security boundary. The policy layer still validates the recommendation, and the application still requires human approval.

## Testing

Command:

```text
python -m pytest tests/test_llm_classifier.py -q
```

Actual output:

```text
.........                                                            [100%]
9 passed in 0.15s
```

The six new adapter tests in `tests/test_llm_classifier.py` pass (the schema-violation test is parametrized, which is why nine cases run):

1. `test_parses_valid_response`
2. `test_parses_markdown_fenced_response`
3. `test_rejects_invalid_json`
4. `test_rejects_schema_violations` (missing field, unexpected field, incorrect type, empty field)
5. `test_rejects_unsupported_priority`
6. `test_wraps_client_failure`

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR collecting tests/test_domain.py
ImportError: cannot import name 'validate_ticket' from 'ticket_triage.domain'
ERROR collecting tests/test_workflow.py
ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow'
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The full suite is still interrupted by the same pre-existing collection errors recorded on Days 6 and 7: `validate_ticket` (`domain.py`) and `transition_case` (`workflow.py`) are referenced but not implemented, and `application.py` still imports `ticket_triage.approval`, which does not exist.

The Day 8 application-integration example was not run. It depends on `TriageApplicationService`, which is still incomplete (`create_case` does not save or return a case; `get_case` and `start_processing` are missing) and on a repository implementation, which does not yet exist. Per the session decision, this was recorded honestly rather than manufactured.

## Limitations

- No real LLM provider is connected yet.
- The fake client does not test network behavior or actual model quality.
- Timeouts, rate limits, token budgets, and provider-specific errors need dedicated handling.
- Prompt instructions do not eliminate prompt-injection risks.
- Ticket content may contain personal or confidential data and must be handled according to the application's privacy requirements.
- The adapter rejects a list where a string is expected, unexpected fields, and empty required fields, but it does not check that `category` and `destination` are in the approved taxonomy; that remains the policy layer's job.

## What I learned

A model integration should be isolated behind an interface. Structured output improves consistency, but deterministic validation and human approval remain necessary.

## Next steps

- Connect a real model provider.
- Configure timeouts and bounded retries.
- Test provider failures and malformed responses at the application boundary.
- Evaluate classification quality on labeled tickets.
- Resolve the Days 6-7 gaps (`validate_ticket`, `transition_case`, repository implementation, and the incomplete application service) so the full suite and the end-to-end integration test can run.

## Day 8 completion checklist

### Progress

3 of 6

- [x] Create llm_classifier.py
- [x] Create the fake LLM client
- [x] Add six adapter tests
- [ ] Verify application integration (blocked by pre-existing application-layer gaps; recorded instead)
- [ ] Run the full test suite (blocked by pre-existing `validate_ticket`/`transition_case` collection errors)
- [x] Write docs/progress/day-08.md