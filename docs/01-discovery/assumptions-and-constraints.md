# Assumptions and Constraints

**Project:** Ticket Triage AI  
**Phase:** 01 — Discovery  
**Status:** Draft — Pending Stakeholder Validation  
**Owner:** AI Architect  
**Last Updated:** 2026-10-10

---

## 1. Purpose

This document records the assumptions, constraints, dependencies, and unresolved questions that could affect the design and implementation of the Ticket Triage AI system.

Its objectives are to:

- Separate confirmed project inputs from unverified assumptions.
- Identify technical, operational, business, and compliance constraints.
- Reduce the risk of making premature architecture decisions.
- Define how assumptions will be validated.
- Establish the information required before Requirements Engineering begins.

**Principle:** No unverified assumption should be treated as an approved requirement or architecture decision.

## 2. Current Project Context

The initial project inputs are:

| Item | Current understanding | Status |
|---|---|---|
| Business objective | Reduce manual ticket triage time | User-provided |
| Expected volume | 1,000–10,000 tickets per day | Initial estimate; validate |
| Automation model | AI recommends; a human approves before routing | User-provided |
| Existing ticketing platform | Not yet identified | Unknown |
| Ticket categories | Not yet documented | Unknown |
| Priority and SLA rules | Not yet documented | Unknown |
| Historical ticket dataset | Availability and quality unknown | Unknown |
| Deployment environment | Not yet selected | Unknown |
| LLM provider | Not yet selected | Unknown |
| Security and privacy requirements | Not yet established | Unknown |

These inputs provide a starting point for discovery. They do not replace stakeholder validation.

## 3. Assumptions Register

Assumptions are beliefs that may influence the solution but have not yet been verified.

| ID | Assumption | Impact if false | Validation method | Status |
|---|---|---|---|---|
| ASM-001 | Ticket descriptions contain enough information to recommend a category. | Classification may be unreliable or require additional data. | Analyze a representative ticket sample. | Open |
| ASM-002 | The organization has a defined set of ticket categories. | A taxonomy must be created or standardized. | Interview the Support Manager and review existing queues. | Open |
| ASM-003 | Routing destinations and ownership rules can be documented. | Recommendations may not map reliably to teams. | Review routing rules and reassignment history. | Open |
| ASM-004 | Human reviewers can approve or correct recommendations. | Review capacity may become a bottleneck. | Map the workflow and measure reviewer availability. | Open |
| ASM-005 | Historical tickets and labels may be available for evaluation. | A labeled evaluation dataset may need to be created. | Inspect data sources and label quality. | Open |
| ASM-006 | The ticketing platform exposes a supported integration mechanism. | Integration may require an alternative design. | Review platform APIs, webhooks, and permissions. | Open |
| ASM-007 | Ticket data may be processed by an approved LLM provider. | Provider, deployment, or model choices may be restricted. | Obtain security, privacy, and legal approval. | Open |
| ASM-008 | AI recommendations can be evaluated against human-reviewed outcomes. | Reliable quality measurement may require a new review process. | Define a labeling and adjudication procedure. | Open |
| ASM-009 | The organization can define acceptable routing and priority error rates. | Production readiness cannot be evaluated objectively. | Agree on risk-based acceptance criteria with stakeholders. | Open |
| ASM-010 | The workflow can continue safely when the model or integration is unavailable. | Failures could interrupt normal ticket handling. | Define and test a manual fallback process. | Open |

### Assumption validation rules

For each assumption:

1. Assign a stakeholder or technical owner.
2. Gather evidence rather than relying on opinion alone.
3. Record the validation result and supporting evidence.
4. Update the status to `Validated`, `Rejected`, or `Partially Validated`.
5. Document any resulting requirement or architecture decision.

A rejected assumption is not necessarily a blocker; it means the design must account for the actual situation.

## 4. Constraints Register

A constraint is a boundary the solution must respect. At this stage, most constraints remain unconfirmed.

| ID | Constraint area | Current constraint or boundary | Status |
|---|---|---|---|
| CON-001 | Human oversight | A human must approve a recommendation before a routing action is executed. | Initial project requirement; confirm workflow details |
| CON-002 | Existing systems | The solution must integrate with the organization's actual ticketing platform. | Platform and integration limits unknown |
| CON-003 | Data privacy | Ticket data must be processed according to applicable organizational policies and legal obligations. | Specific requirements unknown |
| CON-004 | Security | Access to tickets and integration credentials must be appropriately controlled. | Security controls to be defined |
| CON-005 | Reliability | Failure of the AI component must not prevent staff from handling tickets through an approved fallback process. | Proposed design constraint; validate |
| CON-006 | Performance | The system must support the actual average and peak ticket arrival rates. | Workload and latency targets unknown |
| CON-007 | Budget | Model usage, infrastructure, and operational costs must fit an approved budget. | Budget unknown |
| CON-008 | Deployment | The solution must comply with approved hosting, networking, and deployment policies. | Environment and policies unknown |
| CON-009 | Auditability | Recommendations, approvals, corrections, and routing outcomes must be traceable to the extent required by policy. | Required audit scope unknown |
| CON-010 | Maintainability | Category definitions and routing rules should be maintainable without unnecessary application changes. | Proposed design principle |

### Important distinction

Do not assume that a proposed constraint is already an approved organizational policy. In particular, security, data residency, retention, and audit requirements must be confirmed with the responsible stakeholders.

## 5. Technical Unknowns

The following decisions should remain open until discovery provides sufficient evidence.

### 5.1 Ticketing integration

Questions to resolve:

- Which ticketing platform is currently used?
- Does it support REST APIs, webhooks, or event subscriptions?
- Can the system read ticket data and submit recommendations separately from executing routing actions?
- Are API rate limits, permission restrictions, or additional licensing costs involved?
- Does the platform support idempotent updates or another mechanism to prevent duplicate actions?

**Architecture implication:** The integration layer should isolate platform-specific behavior from classification and policy logic.

### 5.2 Model and inference

Questions to resolve:

- Which model providers and deployment options are approved?
- Can ticket data leave the organization's controlled environment?
- What latency and cost are acceptable?
- Are structured outputs supported and sufficiently reliable?
- What happens when model output is incomplete, invalid, or unavailable?
- Is retrieval from internal knowledge sources actually needed?

**Architecture implication:** Keep the model behind an interface so that provider selection does not unnecessarily couple the entire application to one vendor.

Do not introduce a vector database, retrieval pipeline, or multi-agent framework unless a demonstrated requirement justifies it.

### 5.3 Data and evaluation

Questions to resolve:

- Are historical tickets accessible?
- Are category and priority labels reliable?
- Do labels represent the original decision or the final corrected outcome?
- Are some categories much rarer or more costly to misclassify?
- How will sensitive information be removed or protected in test datasets?
- Who adjudicates disagreements between the model and human reviewers?

**Architecture implication:** Establish a representative, versioned evaluation dataset before choosing a model based on a small number of examples.

### 5.4 Scale and performance

The initial estimate is 1,000–10,000 tickets per day.

For context, this is approximately 0.012–0.116 tickets per second when averaged across a full day. This average does **not** establish the required capacity: bursts, business-hour concentration, retries, and downstream rate limits may produce much higher peaks.

Discovery must establish:

- Peak arrivals per minute.
- Ticket text size and attachment behavior.
- Required recommendation latency, including the measurement boundary.
- Expected concurrent requests.
- Retry and timeout policies.
- Availability and recovery expectations.

**Architecture implication:** Do not select queues, worker counts, or infrastructure capacity from daily volume alone.

## 6. Operational and Business Unknowns

| ID | Question | Why it matters |
|---|---|---|
| UNK-001 | What is the current median and p95 active triage time? | Establishes the baseline for time savings. |
| UNK-002 | How often are tickets routed incorrectly or reassigned? | Establishes the baseline for routing quality. |
| UNK-003 | How are priority levels defined, especially for urgent tickets? | Prevents vague or inconsistent priority recommendations. |
| UNK-004 | Who can approve, override, or reject a recommendation? | Defines roles and authorization boundaries. |
| UNK-005 | What happens when an approver is unavailable? | Defines safe queueing and fallback behavior. |
| UNK-006 | Which ticket categories are in scope for the first release? | Controls project scope and evaluation complexity. |
| UNK-007 | What is the acceptable cost per successfully triaged ticket? | Informs model and infrastructure choices. |
| UNK-008 | What are the required service hours and availability targets? | Informs operational design. |
| UNK-009 | What retention and audit periods apply? | Influences logging, storage, and compliance. |
| UNK-010 | How will staff be trained and informed about AI recommendations? | Reduces inconsistent usage and overreliance on model output. |

## 7. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RSK-001 | Incorrect routing recommendations | Unknown | High | Evaluate by category; retain human approval and correction. |
| RSK-002 | Urgent tickets receive insufficient priority | Unknown | Critical | Define urgent-ticket rules and test false negatives separately. |
| RSK-003 | Poor historical labels distort evaluation | Unknown | High | Audit label quality and use human adjudication. |
| RSK-004 | Sensitive ticket information reaches an unapproved provider | Unknown | Critical | Validate data handling, access controls, and provider approval before processing. |
| RSK-005 | Human review becomes a bottleneck | Unknown | High | Measure review time and queue growth during the pilot. |
| RSK-006 | Model output changes or becomes invalid | Medium, provisional | Medium–High | Validate schemas, version prompts and models, and provide a safe fallback. |
| RSK-007 | Cost grows beyond expectations | Unknown | Medium–High | Measure usage and cost per successfully triaged ticket. |
| RSK-008 | Integration failures create duplicate or missing updates | Unknown | High | Define retries, idempotency, reconciliation, and monitoring. |

Likelihood ratings are provisional. Update them after evidence is collected.

## 8. Provisional Design Guardrails

Until discovery is complete, use these guardrails when exploring implementation options:

1. **Human approval remains explicit.** Model output alone must not trigger a routing action.
2. **Validate model output.** Treat generated content as untrusted input; enforce a schema and validate category and priority values.
3. **Keep deterministic rules separate.** Routing permissions, escalation rules, and other mandatory business rules should be enforced by application logic, not solely by a prompt.
4. **Provide a fallback.** When the model or ticketing integration fails, preserve the approved manual workflow.
5. **Maintain traceability.** Record the ticket reference, recommendation, model and prompt versions where appropriate, approval decision, and resulting action, subject to data-retention and privacy policies.
6. **Minimize sensitive data.** Send only the information needed for inference and avoid unnecessarily copying ticket content into logs.
7. **Measure before optimizing.** Establish baseline performance, model quality, and operating cost before committing to numerical improvements.
8. **Keep architecture proportional.** Start with the simplest design that satisfies confirmed requirements; add distributed components or agent orchestration only when justified.

## 9. Validation Plan

| Step | Activity | Expected output |
|---|---|---|
| 1 | Interview Support Manager and frontline agents. | Current workflow, pain points, and routing rules |
| 2 | Inspect representative tickets and available labels. | Data assessment and initial taxonomy |
| 3 | Meet platform engineering and review integration documentation. | Integration feasibility and constraints |
| 4 | Meet security and privacy stakeholders. | Approved data-handling requirements |
| 5 | Measure current triage performance. | Baseline metrics |
| 6 | Define category-specific evaluation criteria. | Evaluation plan and acceptance thresholds |
| 7 | Review assumptions and risks with stakeholders. | Updated registers and decisions |
| 8 | Approve the discovery outputs. | Readiness to begin Requirements Engineering |

## 10. Exit Criteria

Discovery is ready to close when:

- [ ] The business problem and primary users are validated.
- [ ] The current triage workflow is documented.
- [ ] The ticketing platform and integration options are identified.
- [ ] Ticket taxonomy and priority rules are documented or assigned for definition.
- [ ] Historical data availability and quality are assessed.
- [ ] Security, privacy, retention, and provider constraints are reviewed.
- [ ] Baseline triage and routing metrics are measured or a measurement plan is approved.
- [ ] Human approval and failure-handling behavior are agreed.
- [ ] Critical assumptions have evidence-backed outcomes or explicit owners and deadlines.
- [ ] Major risks have owners and mitigation plans.
- [ ] Stakeholders agree on the scope of the first release.

Not every unknown must be eliminated during discovery. However, every unresolved high-impact question must have an owner, a next action, and a deadline before it can safely influence a major architecture decision.

## 11. Change History

| Date | Change | Status |
|---|---|---|
| 2026-10-10 | Initial assumptions and constraints register created. | Draft |

---

**Next step:** Validate this document through stakeholder interviews. Then create the Requirements Engineering artifacts, converting validated business needs and constraints into testable functional and non-functional requirements.
