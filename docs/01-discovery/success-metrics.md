# Success Metrics — AI Ticket Triage

| Field | Value |
|---|---|
| Project | `ticket-triage` |
| Phase | 01 — Discovery |
| Status | Draft — targets pending stakeholder approval |
| Owner | AI Architect |
| Primary business objective | Reduce manual ticket triage time |
| Automation model | AI recommendation followed by human approval |

---

## 1. Purpose

This document defines the metrics used to evaluate whether the AI ticket triage system delivers measurable business value while maintaining acceptable quality, reliability, security, and human oversight.

Metrics will be used to:

- Establish the current business baseline.
- Define measurable pilot acceptance criteria.
- Evaluate classification and routing quality.
- Measure the effect on agent workload.
- Monitor system performance and operating cost.
- Identify quality degradation after deployment.

All proposed numerical targets in this document are initial hypotheses. They must be reviewed against baseline data, ticket characteristics, and business risk before becoming approved requirements.

## 2. Measurement Principles

1. Measure business outcomes, not just model output quality.
2. Compare the AI-assisted workflow against the existing manual process.
3. Use a representative, labeled evaluation dataset.
4. Report results by ticket category and risk level, not only as aggregate averages.
5. Include human review and correction time when calculating time savings.
6. Track failure cases, uncertainty, and escalation behavior.
7. Keep evaluation data separate from training or prompt-development examples where practical.
8. Record metric definitions, measurement periods, data sources, and owners.
9. Avoid treating an LLM's self-reported confidence as a calibrated probability.
10. Do not weaken approval or security controls to improve efficiency metrics.

## 3. Business Metrics

### 3.1 Median Triage Time

**Objective:** Reduce the time support agents spend triaging each ticket.

**Definition:** Median elapsed active triage time per ticket, measured consistently across the baseline and pilot.

For an AI-assisted workflow, include the time required to review, correct, and approve recommendations.

**Formula:**

Reduction percentage =

(Baseline median time − Pilot median time) / Baseline median time × 100

**Proposed target:** At least 30% reduction.

**Data required:**
- Baseline triage duration.
- Pilot triage duration.
- Agent review and correction time.
- Ticket category and complexity.
- Measurement period.

**Owner:** Support manager.

**Important:** Separate active work time from queue waiting time. If elapsed time is used, document which components are included.

### 3.2 Routing Accuracy

**Objective:** Assign tickets to the correct support team.

**Definition:** Percentage of evaluated tickets for which the recommended destination matches the approved reference destination.

**Formula:**

Routing accuracy = Correct destination recommendations / Evaluated tickets × 100

**Proposed target:** At least 95%.

**Owner:** Support operations.

**Evaluation requirement:** Use validated reference labels and report performance by category. Where multiple destinations are valid, define the accepted destinations before evaluation.

### 3.3 Priority Agreement

**Objective:** Ensure that priority recommendations align with the approved business policy.

**Definition:** Percentage of evaluated tickets whose predicted priority matches the approved reference priority.

**Formula:**

Priority agreement = Exact priority matches / Evaluated tickets × 100

**Proposed target:** At least 95%.

**Owner:** Support manager.

**Additional checks:** Track under-prioritization of urgent tickets separately because its business impact may be greater than over-prioritization of a routine ticket.

### 3.4 Human Acceptance Rate

**Objective:** Determine whether recommendations are useful to reviewers.

**Definition:** Percentage of recommendations accepted without modification.

**Formula:**

Acceptance rate = Unmodified accepted recommendations / Recommendations reviewed × 100

**Proposed target:** At least 85%.

**Owner:** Product owner.

**Interpretation:** Acceptance is a usability and workflow metric, not proof of correctness. Validate accepted recommendations against independent reference labels to detect automation bias.

### 3.5 Ticket Reassignment Rate

**Objective:** Reduce avoidable routing errors and rework.

**Definition:** Percentage of tickets that are reassigned after their initial assignment within a defined observation window.

**Formula:**

Reassignment rate = Tickets reassigned within the observation window / Assigned tickets × 100

**Target:** Establish the baseline first; set a reduction target after discovery.

**Owner:** Support operations.

**Note:** Exclude legitimate reassignment caused by changed ownership or new information if the business defines it as non-error-related.

## 4. AI Quality Metrics

| Metric | Definition | Initial target |
|---|---|---|
| Category accuracy | Correct predicted category / Evaluated tickets | Establish after baseline evaluation |
| Per-category precision | Correct predictions for a category / All predictions for that category | Establish per category |
| Per-category recall | Correctly identified examples of a category / All reference examples in that category | Establish per category |
| Macro F1 | Unweighted average of F1 across categories | Establish after baseline evaluation |
| Priority agreement | Exact matches with approved priority labels | At least 95%, proposed |
| Invalid-output rate | Model outputs that fail schema or semantic validation / Model outputs | Establish baseline; minimize |
| Uncertain-case escalation rate | Tickets escalated because evidence is insufficient / Tickets processed | Measure and calibrate against review capacity |

### Why accuracy is not enough

Suppose 90% of tickets belong to routine categories and only 10% involve urgent cases. A model could perform well overall while missing many urgent cases.

For that reason, evaluation must include:
- A confusion matrix.
- Precision and recall for each category.
- Per-priority performance.
- False-negative analysis for urgent cases.
- Performance on ambiguous and incomplete tickets.
- Results on a representative holdout dataset.

For high-impact cases, define acceptable error rates with the business owner rather than assuming that one overall accuracy threshold is sufficient.

## 5. Human Oversight and Safety Metrics

### 5.1 Required Approval Coverage

**Definition:** Percentage of decisions requiring human approval for which the required approval is recorded before the routing action executes.

**Proposed target:** 100%.

**Formula:**

Approval coverage = Decisions with valid prior approval / Decisions requiring approval × 100

**Owner:** Application engineering and support operations.

### 5.2 Decision Traceability

**Definition:** Percentage of triage decisions containing the required decision and approval records.

A record should include, where applicable:
- Ticket reference.
- Model and prompt version.
- Structured recommendation.
- Applicable policy outcome.
- Validation result.
- Reviewer decision and identity.
- Execution status and timestamp.

**Proposed target:** 100% of decisions have the required audit record.

Avoid storing unnecessary ticket content or sensitive information in logs.

### 5.3 Unauthorized Action Rate

**Definition:** Number of unauthorized routing or other prohibited actions executed by the system.

**Target:** Zero.

Enforce this through application permissions, policy checks, and execution controls. Monitoring alone is not a substitute for prevention.

### 5.4 Human Override Rate

**Definition:** Percentage of reviewed recommendations modified or rejected by a human.

**Target:** Establish the baseline during the pilot.

Analyze overrides by category and reason. A high override rate may indicate a model-quality problem, unclear business rules, or a mismatch between the workflow and agent expectations.

## 6. System Performance Metrics

The system is expected to process 1,000–10,000 tickets per day, but peak arrival rates and latency requirements have not yet been confirmed.

| Metric | Definition | Target |
|---|---|---|
| Recommendation latency | Time from accepted ticket submission to available recommendation | Set p95 target after discovery |
| Throughput | Tickets processed per unit of time | Validate peak-load capacity |
| Availability | Time the service meets its defined availability criteria | Establish SLO with IT |
| Processing failure rate | Tickets failing to produce a valid final workflow outcome / Tickets submitted | Establish baseline and error budget |
| Retry recovery rate | Transient failures recovered through permitted retries / Retryable failures | Measure during testing |
| Duplicate action rate | Duplicate routing actions caused by repeated events | Zero unintended duplicate actions |

### Required performance tests

Before production, test:
- Typical and peak ticket volume.
- LLM timeouts and rate limits.
- Invalid or incomplete model outputs.
- Ticketing API outages.
- Duplicate webhook events.
- Database failures.
- Retry exhaustion and recovery.
- Slow or unavailable human-review integrations.

Define latency percentiles and availability measurement rules before accepting a performance result.

## 7. Cost Metrics

### 7.1 Cost per Processed Ticket

**Definition:** Total attributable inference and infrastructure cost divided by the number of tickets processed during the measurement period.

Include:
- LLM input and output usage.
- Application compute.
- Storage and database costs.
- Queueing and observability costs where attributable.
- Additional evaluation or review costs when comparing total operating economics.

**Target:** Establish a cost budget after model and infrastructure options have been evaluated.

### 7.2 Cost per Successfully Triaged Ticket

**Definition:** Total attributable operating cost divided by tickets that reach the agreed successful triage outcome.

This metric helps identify situations where cheap inference produces too many failures, retries, or manual corrections.

### 7.3 Business Value

Estimate net operational benefit using observed time savings and the organization's approved labor-cost assumptions.

Do not count theoretical time savings as realized financial savings unless the business can demonstrate how the recovered capacity is used.

## 8. Baseline and Pilot Evaluation

### Baseline Phase

Collect measurements from the existing manual process.

Record:
- Daily and hourly ticket volume.
- Median and p95 active triage time.
- Routing accuracy or reassignment rate.
- Priority distribution and priority errors.
- Agent workload and review effort.
- Existing operational costs, where available.

If a metric cannot be measured, record the data gap and assign an owner rather than inventing a baseline.

### Offline Evaluation

Before introducing AI recommendations into the live workflow:
1. Assemble representative historical tickets.
2. Obtain validated reference labels.
3. Separate development examples from the evaluation set.
4. Run the proposed classification and routing workflow.
5. Measure per-category and per-priority performance.
6. Inspect critical errors and ambiguous cases.
7. Repeat tests after changes to prompts, models, or policies.

### Controlled Pilot

Run the AI-assisted workflow with human approval.

Compare it with the baseline while accounting for ticket mix, time of day, and workload differences. Collect review time, overrides, failures, and routing outcomes.

Do not remove the human approval requirement merely because an aggregate metric meets its target.

## 9. Metric Ownership

| Responsibility | Owner |
|---|---|
| Business outcomes and triage time | Support manager |
| Routing and priority quality | Support operations |
| Evaluation dataset and AI metrics | AI engineering |
| Application latency and availability | IT / platform engineering |
| Approval and audit coverage | Application engineering |
| Security and access-control verification | Security / privacy |
| Final pilot acceptance | Product owner and business sponsor |

Named owners must be confirmed during stakeholder discovery.

## 10. Initial Metrics Register

| ID | Metric | Baseline | Proposed Target | Status |
|---|---|---|---|---|
| MET-001 | Median triage time | Unknown | 30% reduction | Pending validation |
| MET-002 | Routing accuracy | Unknown | At least 95% | Pending validation |
| MET-003 | Priority agreement | Unknown | At least 95% | Pending validation |
| MET-004 | Unmodified acceptance rate | Unknown | At least 85% | Pending validation |
| MET-005 | Required approval coverage | Unknown | 100% | Proposed control target |
| MET-006 | Decision traceability | Unknown | 100% | Proposed control target |
| MET-007 | Recommendation latency p95 | Unknown | To be agreed | Open |
| MET-008 | Cost per processed ticket | Unknown | Budget to be agreed | Open |
| MET-009 | Ticket reassignment rate | Unknown | Reduction target to be agreed | Open |

## 11. Open Questions

- What is the existing median and p95 triage time?
- How will active work time be measured reliably?
- Which ticket categories require separate quality thresholds?
- What error rate is acceptable for each priority level?
- How many tickets can the human-review process handle?
- What latency and availability SLOs are required?
- What is the acceptable cost per successfully triaged ticket?
- How long should reassignment outcomes be observed?
- Which stakeholders approve the final pilot targets?

## 12. Exit Criteria

This document is ready for approval when:
- [ ] Each metric has a precise definition.
- [ ] Baselines are measured or data gaps are assigned.
- [ ] Pilot targets are reviewed by the appropriate stakeholders.
- [ ] The evaluation dataset and labeling process are defined.
- [ ] High-impact failure modes have explicit acceptance criteria.
- [ ] Metrics have owners and collection methods.
- [ ] The pilot comparison methodology is agreed.
- [ ] Production monitoring requirements are documented.

## 13. Next Step

Proceed to Requirements Engineering.

Translate approved success criteria into testable functional and nonfunctional requirements. Each requirement should reference its metric, acceptance threshold, evaluation method, and owner where applicable.
