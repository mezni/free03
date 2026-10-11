# Day 14 — Configuration Management and Secrets

## Objective

Separate configuration from application code so the same application can run safely in local development, testing, and production environments.

## What I implemented

- Added `config.py` with a pydantic-settings `Settings` model (`APP_ENV`, `TRIAGE_DATABASE_PATH`, `OPENAI_API_KEY`, `OPENAI_MODEL`, `TRIAGE_API_TOKENS`).
- Added `get_settings()` with `lru_cache` and a cache-reset mechanism (`get_settings.cache_clear()`).
- Validated `APP_ENV` with `Literal` and token-registry JSON with a `field_validator`.
- Updated authentication to read the token registry from centralized settings.
- Updated the OpenAI client constructor to read the model and key from settings; the key is required only when constructing a real client (dependency-injected clients skip it).
- Updated `main.py` to use the configured database path and removed redundant `load_dotenv()` (BaseSettings loads `.env`).
- Updated `.env.example` and `.gitignore` (`!.env.example` exception; `ticket_triage.db` already covered by `*.db`).
- Added `pydantic-settings>=2.0.0` to `pyproject.toml`.
- Added configuration tests.

## Concepts learned

- Configuration and business logic should be separated; `config.py` is the single source of truth.
- Environment variables override default settings.
- Unit tests should not depend on a developer's `.env` file (tests construct `Settings(_env_file=None)` directly).
- Secrets must not be committed to source control (`.env` ignored, `.env.example` tracked via exception).
- Configuration validation does not replace secure secrets management.
- Local development credentials must not be treated as production authentication.

## Validation

```text
$ python -m pytest tests/test_config.py tests/test_auth.py tests/test_openai_client.py tests/test_llm_classifier.py -q
.....................                                                    [100%]
21 passed in 5.09s
```

Configuration tests pass (4): defaults, environment-variable override, invalid `APP_ENV`, invalid token-registry JSON. Existing auth and provider tests still pass after the refactor.

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR tests/test_api.py                       ModuleNotFoundError ticket_triage.approval
ERROR tests/test_domain.py                    ImportError validate_ticket
ERROR tests/test_workflow.py                  ImportError transition_case
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The full suite is still interrupted by the same pre-existing collection errors from Days 6-7. The `main.py` startup path cannot run yet because `sqlite_repository.py` and the application layer are incomplete; the configuration layer itself is verified independently.

## Limitations

- `.gitignore` does not remove secrets already committed; a real key in Git history must be revoked/rotated.
- The token registry remains a local-development mechanism, not a production identity provider.
- No environment-specific policy profiles (e.g., different allowlists per environment) beyond `APP_ENV` yet.
- Configuration validation does not replace secure secrets management (secret manager, rotation, audit).

## Validation checklist

- [x] Configuration tests pass.
- [ ] Full test suite passes (blocked by pre-existing Days 6-7 collection errors).
- [x] App configuration loads without an OpenAI API key (key optional at settings level; only required by the real client).
- [x] Invalid environment values fail validation.
- [x] Invalid token-registry JSON fails validation.
- [x] `.env` is excluded from Git; `.env.example` is tracked.
- [x] Existing API authentication logic tests still pass.

## Reflection

- **Why central configuration over scattered `os.environ` reads?** One validated, typed source of truth; the same code runs across environments; deterministic behavior in tests; failures surface at startup instead of deep in a request.
- **Validating configuration vs. securely managing secrets:** validation checks shape and presence; secure management covers storage, access control, rotation, auditing, and preventing exposure. A valid-looking key can still be leaked or over-privileged.

## Next

Day 15 — Integration testing and end-to-end workflow validation.

## Day 14 completion checklist

### Progress

- [x] Install and declare `pydantic-settings`
- [x] Create `config.py`
- [x] Update `auth.py` to use settings
- [x] Update `openai_client.py` to use settings
- [x] Update `main.py` to use configured database path
- [x] Update `.env.example` and `.gitignore`
- [x] Add `tests/test_config.py` (4 tests)
- [x] Run the full test suite (recorded; blocked by pre-existing collection errors)
- [x] Write `docs/progress/day-14.md`