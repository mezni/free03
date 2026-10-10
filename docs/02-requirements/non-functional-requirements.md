# Non-Functional Requirements

**Project:** Ticket Triage AI  
**Status:** Draft — Targets Pending Validation

## 1. Purpose

Define the quality attributes and operational characteristics the system must satisfy.

A non-functional requirement should be measurable wherever practical. Terms such as "fast," "secure," and "reliable" are insufficient without a verification method.

## 2. Requirements

### NFR-001 — Performance

**Priority:** Must have

The system must generate recommendations within an agreed latency target under the expected workload.

**Measurement:**
- Measure p50, p95, and p99 recommendation latency.
- Define whether the measurement includes ticket ingestion, model inference, validation, and presentation.
- Test under representative and peak workloads.

**Target:** To be determined during discovery.

### NFR-002 — Classification Quality

**Priority:** Must have

The system must meet stakeholder-approved classification and routing quality thresholds.

**Measurement:**
- Evaluate on a representative held-out dataset.
- Measure category-level precision and recall.
- Report confusion matrices.
- Measure routing accuracy and priority agreement.
- Report urgent-ticket false negatives separately.

**Initial proposed targets:** At least 95% routing accuracy and 95% priority agreement. These are hypotheses, not approved production commitments.

### NFR-003 — Human Oversight

**Priority:** Must have

The system must enforce the required approval step before routing.

**Acceptance target:** 100% of routing actions subject to approval must have a valid recorded approval.

### NFR-004 — Reliability and Recovery

**Priority:** Must have

The system must handle dependency failures without losing track of tickets or executing unauthorized actions.

**Measurement:**
- Test model timeouts and malformed responses.
- Test ticketing API failures.
- Test safe retries and duplicate submissions.
- Verify that unresolved tickets can enter the approved manual workflow.

**Target:** Recovery time and availability objectives to be agreed.

### NFR-005 — Security

**Priority:** Must have

The system must enforce appropriate authentication, authorization, secret management, and least-privilege access.

**Verification:**
- Review access controls.
- Test unauthorized approval and routing attempts.
- Verify that credentials are not exposed in logs or source control.
- Review dependencies and deployment configuration.

### NFR-006 — Privacy and Data Handling

**Priority:** Must have

Ticket data must be processed, stored, and logged in accordance with approved organizational and legal requirements.

**Verification:**
- Confirm permitted model providers and processing locations.
- Define retention and deletion rules.
- Minimize sensitive information in logs.
- Verify approved handling of test datasets.

### NFR-007 — Auditability

**Priority:** Must have

The system must maintain sufficient traceability to reconstruct relevant recommendation and approval events.

**Verification:**
- Confirm that required events are recorded.
- Verify event ordering and timestamps.
- Check that logs are protected against unauthorized modification.
- Confirm retention and access policies.

### NFR-008 — Scalability

**Priority:** Must have

The system must support measured peak workload, not just average daily ticket volume.

**Workload input:** Initial estimate of 1,000–10,000 tickets per day.

**Verification:**
- Establish peak arrival rates.
- Load-test representative ticket sizes.
- Measure throughput, latency, and error rates.
- Evaluate ticketing API limits and model-provider quotas.

### NFR-009 — Maintainability

**Priority:** Should have

Classification, validation, routing policy, model integration, and ticketing integration should be separated into testable components.

**Verification:**
- Unit-test business rules independently.
- Verify that changing routing rules does not require rewriting the model integration.
- Document configuration and operational procedures.

### NFR-010 — Observability

**Priority:** Must have for a production deployment

The system must provide sufficient metrics, structured logs, and alerts to detect operational failures.

Monitoring must avoid unnecessarily exposing sensitive ticket content.

### NFR-011 — Cost Efficiency

**Priority:** Must have

The system must operate within an approved budget.

**Measurement:**
- Measure model and infrastructure costs.
- Calculate cost per successfully triaged ticket.
- Include retries, failed requests, and human review effort where relevant.

**Target:** To be determined with business stakeholders.

## 3. Quality Measurement Principles

- Use a held-out evaluation dataset to avoid evaluating only on examples used during development.
- Report performance by category, priority, and relevant risk group.
- Do not use overall accuracy alone to establish safety.
- Do not treat human acceptance as proof that a recommendation is correct.
- Do not use model-reported confidence as a calibrated probability without validation.
- Record the model, prompt, dataset, and evaluation configuration used for each evaluation.

## 4. Approval Requirements

Before production readiness can be assessed, stakeholders must approve:

- Latency and availability objectives.
- Classification and routing acceptance thresholds.
- Urgent-ticket handling criteria.
- Security and privacy controls.
- Recovery expectations.
- Operating cost limits.

Unapproved targets must remain explicitly marked as provisional.