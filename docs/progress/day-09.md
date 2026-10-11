# Day 9 — Real LLM Provider Integration

## Objective

Connect a real LLM provider while preserving the provider-neutral application architecture.

## Implemented

- Added `OpenAILLMClient`.
- Used the OpenAI Responses API.
- Configured structured output using JSON Schema.
- Made the model configurable through environment variables.
- Added request timeouts and bounded SDK retries.
- Added a fake SDK client for unit testing.
- Added a test that verifies the structured-output request.
- Kept the existing classifier, policy, approval, and routing boundaries.
- Added `openai` and `python-dotenv` to `pyproject.toml` dependencies.
- Added `.env.example`; `.gitignore` already covered `.env`, `.venv/`, caches, and build artifacts.

## Architecture concepts

### Adapter pattern

`OpenAILLMClient` implements the application's `LLMClient` contract. Provider-specific details remain isolated from the domain and application layers.

### Configuration management

Credentials and model selection belong in environment-based configuration, not source code. `OPENAI_MODEL` defaults to `gpt-4o-mini`.

### Resilience

`timeout=20.0` prevents indefinitely waiting for a response. `max_retries=1` bounds repeated requests, but retry policies must still account for latency, cost, and transient versus permanent errors. Provider timeouts and API failures surface as `ClassificationError` through `LLMClassifier`, entering the existing classification-failure path.

### Structured output

JSON Schema constrains the response shape (`json_schema` format with `strict: true`). The application must still validate business policy and treat the recommendation as untrusted until approved.

## Testing

Unit tests use a fake SDK client and require no API key:

```text
$ python -m pytest tests/test_openai_client.py -q
.                                                                  [100%]
1 passed in 5.98s
```

The test verifies that the adapter sends the expected model, prompt, and strict JSON-schema format, and returns the response text.

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR collecting tests/test_domain.py
ImportError: cannot import name 'validate_ticket' from 'ticket_triage.domain'
ERROR collecting tests/test_workflow.py
ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow'
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The full suite is still interrupted by the pre-existing collection errors from Days 6-7 (`validate_ticket` and `transition_case` undefined). The Day 8 adapter tests (9 cases) and the Day 9 provider-adapter test pass when run individually.

The optional synthetic-ticket API smoke test was not run: no `OPENAI_API_KEY` is configured, and the end-to-end application flow still depends on the incomplete application layer (`create_case`/`start_processing`/`classify_case`), consistent with the Day 8 decision to record honestly rather than manufacture results.

## Limitations

- The selected model must support the requested structured-output feature.
- Real provider latency, cost, and classification quality have not yet been measured.
- Production deployment needs secret management, monitoring, privacy review, and appropriate error classification.
- Retry behavior is intentionally coarse; transient versus permanent errors are not yet distinguished.
- Human approval remains mandatory.

## What I learned

A real LLM provider can be integrated without making the application dependent on its SDK. Provider integration is an infrastructure concern, not a business-workflow concern.

## Next steps

- Add observability for latency, failures, and token usage.
- Separate transient provider failures from invalid model output.
- Build a labeled evaluation dataset.
- Measure classification quality before considering automated routing.
- Resolve the Days 6-7 gaps (`validate_ticket`, `transition_case`, repository implementation, incomplete application service) so the full suite and a real end-to-end smoke test can run.

## Day 9 completion checklist

### Progress

4 of 6

- [x] Add OpenAILLMClient
- [x] Configure environment variables and .gitignore (`.env.example` created; `.gitignore` already complete)
- [x] Add the fake-SDK unit test
- [x] Run the full test suite (recorded; still blocked by pre-existing collection errors)
- [ ] Optionally run one synthetic-ticket API test (not run: no API key configured)
- [x] Write docs/progress/day-09.md