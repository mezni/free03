# API Contracts — Ticket Triage AI

## 1. Purpose

This document defines the initial REST API contract for the Ticket Triage AI backend.

It specifies:
- API endpoints and HTTP methods.
- Request and response schemas.
- Authentication and authorization requirements.
- Validation and error handling.
- Approval and routing safeguards.
- Idempotency and concurrency behavior.

These contracts are provisional. They must be aligned with the selected ticketing platform, identity provider, and implementation framework before production use.

## 2. API Design Principles

1. Use resource-oriented REST endpoints.
2. Represent identifiers explicitly and consistently.
3. Validate all requests and responses at the backend boundary.
4. Return structured errors with stable error codes.
5. Require authentication for protected operations.
6. Enforce authorization and workflow state transitions on the server.
7. Require explicit human approval before routing.
8. Use idempotency controls for operations that may be retried.
9. Avoid exposing internal exceptions, secrets, or unnecessary ticket data.
10. Version the API to support controlled evolution.

Base path:

`/api/v1`

Content type:

`application/json`

All timestamps use ISO 8601 format in UTC unless a contract explicitly states otherwise.

## 3. Endpoint Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/tickets` | Register or submit a ticket for triage |
| `GET` | `/triage-cases/{case_id}` | Retrieve case status and current recommendation |
| `GET` | `/triage-cases` | List cases available to an authorized reviewer |
| `POST` | `/triage-cases/{case_id}/decisions` | Approve, correct, or reject a recommendation |
| `GET` | `/triage-cases/{case_id}/routing` | Retrieve routing-operation status |
| `POST` | `/triage-cases/{case_id}/retry` | Request a permitted recovery action |

The retry endpoint is intended for controlled recovery, not arbitrary repetition of external side effects. It should only be implemented if operational requirements justify it.

Ticketing-platform webhooks may use a separate integration endpoint once the platform and its authentication mechanism are selected.

## 4. Common Response Conventions

### 4.1 Successful Response

A successful request returns a response appropriate to the endpoint, usually with a `2xx` HTTP status.

For example:

```json
{
  "case_id": "case_123",
  "status": "pending_approval",
  "created_at": "2026-10-10T14:30:00Z"
}
```

Identifiers shown in this document are illustrative.

### 4.2 Error Response

Errors should use a consistent structure.

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request contains invalid fields.",
    "request_id": "req_abc123",
    "details": [
      {
        "field": "ticket.subject",
        "reason": "required"
      }
    ]
  }
}
```

The `message` should be safe to return to the caller. Internal exception details belong in protected logs, not in API responses.

## 5. Endpoint Contracts

### 5.1 Submit a Ticket for Triage

**Endpoint:** `POST /api/v1/tickets`

**Purpose:** Register a ticket and initiate its triage workflow.

Authentication: required.

Authorization: caller must have permission to submit tickets for triage.

Request:

```json
{
  "source_system": "support-platform",
  "external_ticket_id": "TCK-10025",
  "ticket": {
    "subject": "Unable to sign in",
    "description": "The customer cannot access their account.",
    "customer_tier": "standard"
  }
}
```

The example ticket fields are illustrative. The final schema must match the source platform and approved data-minimization rules.

Successful response — `202 Accepted`:

```json
{
  "case_id": "case_123",
  "status": "received",
  "request_id": "req_abc123"
}
```

`202 Accepted` means the request has been accepted for processing, not that classification or routing has completed.

Expected errors:

- `400 Bad Request` — malformed request.
- `401 Unauthorized` — missing or invalid authentication.
- `403 Forbidden` — caller lacks permission.
- `409 Conflict` — incompatible duplicate or conflicting ticket state.
- `422 Unprocessable Content` — structurally valid request that violates business validation.
- `429 Too Many Requests` — rate limit exceeded.
- `503 Service Unavailable` — required dependency is unavailable and the request cannot be accepted safely.

Duplicate submissions must be handled according to the source ticket identity and idempotency policy. A duplicate should not create an independent routing action.

### 5.2 Retrieve a Triage Case

**Endpoint:** `GET /api/v1/triage-cases/{case_id}`

**Purpose:** Retrieve workflow status and the current recommendation.

Authentication: required.

Authorization: caller must be allowed to view the case.

Successful response — `200 OK`:

```json
{
  "case_id": "case_123",
  "ticket_reference": {
    "source_system": "support-platform",
    "external_ticket_id": "TCK-10025"
  },
  "status": "pending_approval",
  "current_recommendation": {
    "recommendation_id": "rec_456",
    "version": 1,
    "category": "account_access",
    "priority": "high",
    "destination": "identity_support",
    "rationale": "The ticket describes an account sign-in failure.",
    "validation_status": "valid"
  },
  "created_at": "2026-10-10T14:30:00Z",
  "updated_at": "2026-10-10T14:30:05Z"
}
```

Expected errors:

- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`

Do not expose recommendation details to callers who are not authorized to access the ticket.

### 5.3 List Triage Cases

**Endpoint:** `GET /api/v1/triage-cases`

**Purpose:** Return a paginated list of cases available to the caller.

Possible query parameters:

- `status` — filter by workflow status.
- `limit` — maximum number of results.
- `cursor` — pagination cursor.

Example:

`GET /api/v1/triage-cases?status=pending_approval&limit=25`

Successful response — `200 OK`:

```json
{
  "items": [
    {
      "case_id": "case_123",
      "external_ticket_id": "TCK-10025",
      "status": "pending_approval",
      "priority": "high",
      "created_at": "2026-10-10T14:30:00Z"
    }
  ],
  "next_cursor": null
}
```

Expected errors:

- `400 Bad Request` — invalid filter or pagination value.
- `401 Unauthorized`
- `403 Forbidden`

Apply authorization and pagination limits on the server. Do not rely on frontend filtering to enforce access restrictions.

### 5.4 Record a Human Decision

**Endpoint:** `POST /api/v1/triage-cases/{case_id}/decisions`

**Purpose:** Approve, correct, or reject the current recommendation.

Authentication: required.

Authorization: the authenticated actor must have the appropriate reviewer role.

Request — approval:

```json
{
  "recommendation_id": "rec_456",
  "recommendation_version": 1,
  "decision": "approved",
  "comment": "Reviewed and accepted."
}
```

Request — correction:

```json
{
  "recommendation_id": "rec_456",
  "recommendation_version": 1,
  "decision": "corrected",
  "correction": {
    "category": "account_access",
    "priority": "medium",
    "destination": "general_support"
  },
  "comment": "The issue does not meet the high-priority criteria."
}
```

Request — rejection:

```json
{
  "recommendation_id": "rec_456",
  "recommendation_version": 1,
  "decision": "rejected",
  "comment": "Insufficient information for automated triage."
}
```

Correction fields must be validated against the configured category taxonomy, priority rules, and destination list.

The server obtains the actor identity from authenticated credentials. It must not trust an `actor_id` supplied by the request body.

Successful response — `201 Created`:

```json
{
  "decision_id": "dec_789",
  "case_id": "case_123",
  "decision": "approved",
  "recommendation_id": "rec_456",
  "recommendation_version": 1,
  "recorded_at": "2026-10-10T14:35:00Z"
}
```

Expected errors:

- `400 Bad Request` — malformed decision.
- `401 Unauthorized`
- `403 Forbidden` — insufficient reviewer permissions.
- `404 Not Found` — case or recommendation does not exist or is not visible to the caller.
- `409 Conflict` — recommendation version is stale, the case is no longer eligible, or a conflicting decision already exists.
- `422 Unprocessable Content` — invalid correction values.

The server must atomically validate the current case state, verify the recommendation version, and persist the decision. Approval of one recommendation version must not authorize routing of a later version.

### 5.5 Retrieve Routing Status

**Endpoint:** `GET /api/v1/triage-cases/{case_id}/routing`

**Purpose:** Retrieve the state of routing operations for a case.

Authentication: required.

Authorization: caller must have permission to view the case and its operational status.

Successful response — `200 OK`:

```json
{
  "case_id": "case_123",
  "operations": [
    {
      "operation_id": "route_001",
      "status": "succeeded",
      "attempt_count": 1,
      "updated_at": "2026-10-10T14:35:10Z"
    }
  ]
}
```

Possible routing statuses include:

- `pending`
- `in_progress`
- `succeeded`
- `failed`
- `outcome_unknown`
- `reconciliation_required`

A routing status of `outcome_unknown` means the system cannot yet confirm whether the external update occurred. It must not be displayed as a confirmed failure or success.

Expected errors:

- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`

### 5.6 Request Recovery

**Endpoint:** `POST /api/v1/triage-cases/{case_id}/retry`

**Purpose:** Request a controlled recovery action when an operation is eligible for retry.

This endpoint is optional and must not be exposed to ordinary reviewers unless their role explicitly permits the action.

Request:

```json
{
  "operation_id": "route_001",
  "reason": "External system failure was investigated."
}
```

Successful response — `202 Accepted`:

```json
{
  "operation_id": "route_001",
  "status": "pending",
  "request_id": "req_retry_001"
}
```

The backend must inspect the operation state before accepting recovery. If the previous routing outcome is unknown, reconcile the external state before retrying unless the target platform guarantees safe idempotent behavior.

Expected errors:

- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict` — operation is not eligible for recovery.
- `422 Unprocessable Content` — invalid recovery request.

A recovery request must never bypass the approval requirement.

## 6. Authentication and Authorization

The implementation must use the organization's approved authentication mechanism.

Possible approaches include:
- Existing ticketing-platform identity and session integration.
- OAuth 2.0 or OpenID Connect for user authentication.
- Service credentials for trusted platform-to-platform integrations.

Authorization must be enforced on the backend for every protected operation.

Example permission model:

| Action | Required Permission |
|---|---|
| Submit a ticket | `triage:submit` |
| View a case | `triage:read` |
| Review a recommendation | `triage:review` |
| Approve or reject | `triage:decide` |
| Correct a recommendation | `triage:correct` |
| Request recovery | `triage:recover` |
| Configure policy | `triage:admin` |

These permission names are illustrative and must be aligned with the organization's identity model.

Integration endpoints must verify the source of inbound requests. Publicly reachable webhook endpoints must not trust a request merely because it contains a ticket identifier.

## 7. Idempotency and Concurrency

Operations that may be repeated because of retries or network failures need explicit duplicate-handling rules.

For ticket submission:
- Use the source system and external ticket ID to identify duplicate events.
- Return the existing case or a documented conflict response when appropriate.
- Avoid creating duplicate active workflows for the same event.

For decision recording:
- Verify that the case and recommendation version are still eligible.
- Prevent conflicting decisions from being committed concurrently.
- Use an idempotency key if the client may retry after an uncertain response.

For routing:
- Generate and persist a stable idempotency key for each logical operation.
- Reuse that key only when retrying the same logical operation.
- Verify the external operation outcome before repeating an action whose result is unknown.

HTTP idempotency behavior must be documented for each endpoint where it applies.

## 8. Error Handling and Observability

Each request should have a correlation or request ID that connects API activity to relevant workflow events.

Log:
- Request and correlation IDs.
- Endpoint and outcome.
- Duration and dependency latency.
- Sanitized error codes.
- Relevant workflow identifiers.

Do not log authentication tokens, secrets, or unnecessary ticket content.

Recommended error codes include:

| Code | Meaning |
|---|---|
| `INVALID_REQUEST` | Request format or fields are invalid |
| `UNAUTHENTICATED` | Authentication is missing or invalid |
| `FORBIDDEN` | Caller lacks permission |
| `NOT_FOUND` | Resource is unavailable or not visible |
| `INVALID_STATE` | Operation is not allowed in the current state |
| `VERSION_CONFLICT` | Request references a stale version |
| `DEPENDENCY_UNAVAILABLE` | A required external dependency is unavailable |
| `OUTCOME_UNKNOWN` | External operation outcome is unresolved |
| `RATE_LIMITED` | Caller exceeded an applicable rate limit |

Use HTTP status codes consistently with these error codes.

## 9. API Contract Testing

The implementation must test at least the following scenarios:

1. A valid ticket submission is accepted.
2. A duplicate ticket event does not create a duplicate workflow.
3. Invalid ticket data is rejected.
4. Unauthorized callers cannot view protected cases.
5. A valid recommendation can be retrieved by an authorized reviewer.
6. An authorized reviewer can approve an eligible recommendation.
7. A stale recommendation version cannot be approved.
8. A corrected recommendation is validated against business rules.
9. An unauthorized actor cannot approve or route a ticket.
10. A rejected recommendation cannot trigger routing.
11. A routing timeout is represented as unresolved when success or failure cannot be established.
12. Concurrent decision requests cannot create conflicting approvals.
13. Recovery cannot bypass approval or idempotency safeguards.
14. Error responses do not expose secrets or sensitive internal details.

## 10. Open Questions

| ID | Question | Impact |
|---|---|---|
| API-001 | Which authentication protocol is required? | Determines authentication integration |
| API-002 | Which ticket fields are mandatory? | Determines request schemas |
| API-003 | How does the ticketing platform authenticate webhooks? | Determines integration security |
| API-004 | Should ticket submission be synchronous or asynchronous? | Determines response and processing behavior |
| API-005 | What pagination and filtering does the review interface need? | Determines listing contract |
| API-006 | Which actions may reviewers and administrators perform? | Determines authorization rules |
| API-007 | Does the target platform support idempotency keys or operation lookup? | Determines routing recovery behavior |

## 11. Exit Criteria

This document is ready for implementation planning when:
- Endpoint responsibilities and request/response schemas are understood.
- Authentication and authorization expectations are documented.
- Decision and routing safeguards are explicit.
- Duplicate requests and concurrent operations have defined behavior.
- Error responses are consistent and safe.
- Open integration questions are tracked.

## 12. Next Document

Create `docs/03-system-design/deployment-architecture.md`.

That document will describe the proposed runtime environment, deployment boundaries, configuration and secrets management, network access, scaling considerations, and operational dependencies. Technology-specific choices remain provisional until the project's constraints are validated.
