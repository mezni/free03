# Day 13 — Authentication and Authorization

## Objective

Protect the ticket-triage API using authentication and role-based access control (RBAC).

## What I implemented

- Added a `Principal` model containing the authenticated subject and roles.
- Added bearer-token authentication using a local development token registry (`TRIAGE_API_TOKENS` in the environment).
- Added a reusable `require_roles()` authorization dependency.
- Protected ticket creation, classification, reading, and approval endpoints.
- Added an approval request schema (`DecisionRequest`) that rejects unexpected fields and has no `actor_id` field.
- Obtained reviewer identity from the authenticated principal instead of trusting the request body.
- Added tests for unauthenticated access, forbidden approval, and actor-identity spoofing intent.
- Added `tests/test_auth.py` so authentication/authorization logic runs and passes (5 tests).
- Added example tokens to `.env.example` (local development only).

## Authorization matrix

| Operation | Allowed roles |
|---|---|
| `GET /health` | Public |
| `POST /cases` | submitter, admin |
| `GET /cases/{case_id}` | Any authenticated caller |
| `POST /cases/{case_id}/classify` | submitter, admin, system |
| `POST /cases/{case_id}/decision` | reviewer, admin |

`get_current_principal` reads the token registry from `TRIAGE_API_TOKENS`; a missing or unknown token yields 401, and a known token yields a `Principal`. `require_roles` yields 403 when the caller lacks any required role.

## Concepts learned

- Authentication establishes identity; authorization checks permissions.
- HTTP 401 indicates missing or invalid credentials; HTTP 403 indicates insufficient permissions.
- RBAC associates permissions with roles.
- Request validation and business-rule validation solve different problems.
- Authentication does not automatically grant access to every record.
- A development token registry is not a production identity provider.

## Testing

```text
$ python -m pytest tests/test_auth.py -q
.....                                                                    [100%]
5 passed in 1.78s
```

The five auth tests cover authorized roles, forbidden roles (403), missing credentials (401), unknown tokens (401), and known-token principal construction.

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR tests/test_api.py                       ModuleNotFoundError ticket_triage.approval
ERROR tests/test_domain.py                    ImportError validate_ticket
ERROR tests/test_workflow.py                  ImportError transition_case
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The API-level tests (`tests/test_api.py`, now including the 401/403 checks and the `get_current_principal` dependency override) cannot execute because `api.py` imports the application layer, which still depends on the missing `ticket_triage.approval` module (Days 6-7 gap). This was recorded per the prior session decision; the endpoint patterns, dependency override, and role matrix are implemented as specified.

## Security limitations

- The token registry is intended only for local learning.
- Case-level ownership and tenant isolation are not implemented.
- Identity-provider integration, token expiry, and token rotation remain future work.
- Administrative permissions require further definition.
- Routing authorization and durable audit records need additional work.

## Validation

- Run the full test suite: still interrupted at collection by the Days 6-7 gaps.
- Verify unauthenticated requests receive 401: auth module tests confirm the dependency behavior.
- Verify submitters cannot approve cases: implemented and asserted in `test_api.py` (cannot run until the application layer is importable).
- Verify reviewers can approve eligible cases: implemented in the decision endpoint; not executable yet.
- Verify request bodies cannot spoof reviewer identity: `DecisionRequest` has no `actor_id`; the endpoint uses `principal.subject`.
- Confirm existing approval and routing safeguards still pass: blocked by the same missing modules.

## Reflection

- **Authentication vs. authorization vs. business-rule validation:** authentication answers "who are you?", authorization answers "what roles allow you to do?", and business-rule validation enforces workflow invariants (e.g., a case cannot be approved twice, routing requires approval for the current recommendation version). Each is a distinct boundary.
- **Why must reviewer identity come from the authenticated principal?** The HTTP request is user-controlled. Trusting a body-supplied `actor_id` lets a caller claim any reviewer's identity and record decisions they are not authorized to make.

## Next

Day 14 — Configuration management, secrets handling, and environment separation.

## Day 13 completion checklist

### Progress

Per the session decision, API runtime tests are recorded as blocked; auth logic itself is verified.

- [x] Add authentication module (`auth.py`) — verified by `tests/test_auth.py`
- [x] Protect API endpoints with role dependencies
- [x] Add approval decision endpoint and schema
- [x] Keep `/health` public
- [x] Add API tests with principal override and auth checks (created; not executable while the application layer is missing)
- [x] Update `.env.example` with local dev tokens
- [x] Run the full test suite (recorded; blocked by pre-existing collection errors)
- [x] Write docs/progress/day-13.md