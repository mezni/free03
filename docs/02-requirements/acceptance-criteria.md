# Acceptance Criteria

**Project:** Ticket Triage AI  
**Status:** Draft — Pending Stakeholder Validation

## 1. Purpose

Define observable conditions that demonstrate whether the system meets its functional and non-functional requirements.

## 2. Acceptance Scenarios

### AC-001 — Valid Ticket

**Given** a ticket contains all required fields,

**When** the system receives it,

**Then** the system validates and normalizes the ticket before classification.

### AC-002 — Missing Required Data

**Given** a ticket is missing a mandatory field,

**When** the system processes it,

**Then** the system rejects or quarantines the ticket according to the defined input policy and records the reason.

### AC-003 — Valid Classification

**Given** a supported ticket is available,

**When** classification succeeds,

**Then** the system returns a category from the approved taxonomy in the required output schema.

### AC-004 — Invalid Model Output

**Given** the model returns malformed output or an unsupported category,

**When** the system validates the response,

**Then** the response is not accepted as a valid recommendation, and the configured retry or manual fallback policy is applied.

### AC-005 — Human Approval

**Given** a valid recommendation is awaiting review,

**When** an authorized reviewer approves it,

**Then** the system records the decision and may proceed to the routing step.

### AC-006 — Rejected Recommendation

**Given** a recommendation is awaiting review,

**When** the reviewer rejects or corrects it,

**Then** the original recommendation must not trigger routing, and the resulting decision must be recorded.

### AC-007 — No Approval

**Given** a recommendation has not been approved,

**When** a routing action is requested,

**Then** the system refuses to execute the action.

### AC-008 — Unauthorized Approval

**Given** a user does not have approval permission,

**When** the user attempts to approve a recommendation,

**Then** the approval is denied and the attempt is handled according to the security logging policy.

### AC-009 — Model Timeout

**Given** the model does not respond within the configured timeout,

**When** processing reaches the timeout limit,

**Then** the system follows the retry policy or transfers the ticket to the approved fallback workflow without routing it automatically.

### AC-010 — Ticketing API Failure

**Given** a reviewer has approved a recommendation,

**When** the ticketing platform fails to execute the routing action,

**Then** the system records the failure, applies safe retry or reconciliation behavior, and avoids silently treating the routing as successful.

### AC-011 — Duplicate Submission

**Given** the same routing request is submitted more than once,

**When** the system processes the duplicate,

**Then** it prevents duplicate side effects where supported and records the final outcome.

### AC-012 — Auditability

**Given** a recommendation has been processed,

**When** an authorized operator inspects the audit record,

**Then** the operator can determine the recommendation, approval decision, and routing outcome from the permitted records.

## 3. Evaluation Acceptance

Before a pilot can be approved:

- [ ] A representative evaluation dataset has been defined.
- [ ] Dataset labels have been reviewed for quality.
- [ ] Routing accuracy has been measured.
- [ ] Priority agreement has been measured.
- [ ] Urgent-ticket false negatives have been assessed separately.
- [ ] Category-level precision and recall have been reported.
- [ ] Latency and operating cost have been measured.
- [ ] Human approval and fallback behavior have been tested.
- [ ] Stakeholders have approved the thresholds used to judge readiness.

## 4. Requirement Traceability

| Acceptance criterion | Requirement |
|---|---|
| AC-001 | FR-001, FR-002 |
| AC-002 | FR-001 |
| AC-003 | FR-003 |
| AC-004 | FR-006, FR-010 |
| AC-005 | FR-007, FR-008 |
| AC-006 | FR-007, FR-008, FR-009 |
| AC-007 | FR-008 |
| AC-008 | FR-007 |
| AC-009 | FR-010 |
| AC-010 | FR-008, FR-009, FR-010 |
| AC-011 | FR-001, FR-008 |
| AC-012 | FR-009 |

## 5. Approval

The requirements baseline is ready for approval when:

- All Must-have requirements have testable acceptance criteria.
- Provisional numerical targets are clearly distinguished from approved thresholds.
- High-risk failure scenarios have corresponding tests.
- Stakeholders agree on MVP scope.
- Unresolved requirements have named owners and due dates.

**Approval status:** Pending stakeholder review.