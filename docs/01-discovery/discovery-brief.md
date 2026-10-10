# Discovery Brief — AI Ticket Triage System

| Field | Value |
|---|---|
| Project | `ticket-triage` |
| Document status | Draft — pending stakeholder validation |
| Phase | 01 — Discovery |
| Document owner | AI Architect |
| Primary objective | Reduce manual ticket triage time |

## 1. Executive Summary

The `ticket-triage` project aims to reduce the time support agents spend manually classifying and routing incoming customer support tickets.

The proposed solution uses an AI model to analyze ticket content and recommend a category, priority, and responsible support team. A human reviews and approves each recommendation before the corresponding routing action is executed.

The architecture will prioritize measurable business value, reliable recommendations, controlled automation, security, and operational maintainability.

The initial design will remain technology-neutral until stakeholder interviews establish the business requirements, existing platform capabilities, and technical constraints.

## 2. Business Problem

Customer support teams must review incoming tickets, understand customer issues, determine their urgency, and assign them to the appropriate team.

Manual triage can introduce several operational problems:

- Time spent repeatedly reading and categorizing tickets.
- Inconsistent interpretation of categories and priorities.
- Incorrect team assignments and ticket reassignment.
- Delays in identifying urgent issues.
- Limited visibility into triage performance and decision quality.

These are initial problem hypotheses. Stakeholder interviews and operational data must confirm which problems exist and how significant they are.

## 3. Business Objective

The primary objective is to reduce manual ticket triage time while maintaining or improving routing and prioritization quality.

Secondary objectives are to:

- Improve consistency in ticket classification.
- Reduce unnecessary ticket reassignment.
- Provide explainable recommendations to support agents.
- Establish an auditable record of AI recommendations and human decisions.
- Create a measurable foundation for future automation.

## 4. Initial Project Inputs

| Attribute | Initial Value |
|---|---|
| Expected ticket volume | 1,000–10,000 tickets per day |
| Primary business goal | Reduce manual triage time |
| Automation approach | AI recommendation followed by human approval |
| Existing ticketing platform | Not yet identified |
| Ticket categories and routing rules | Not yet documented |
| Historical labeled data | Availability unknown |
| Deployment environment | Undetermined |
| Budget and cost constraints | Undetermined |
| Security and privacy constraints | To be established |

The ticket volume and operating model are initial project inputs. They do not yet constitute a complete set of validated system requirements.

## 5. Proposed Solution

The initial solution will provide an AI-assisted ticket triage workflow.

For each incoming ticket, the system will aim to:

1. Validate and normalize the ticket data.
2. Analyze the ticket content.
3. Recommend a category and subcategory.
4. Recommend a priority based on the agreed business policy.
5. Recommend a responsible support team.
6. Produce a concise summary and identify missing information.
7. Validate the recommendation against defined rules.
8. Present the recommendation to an authorized human reviewer.
9. Execute the approved routing action.
10. Record the recommendation, approval decision, and execution outcome.

The system must support a safe failure path when the model produces invalid output, confidence is insufficient, required information is missing, or a downstream integration fails.

Confidence scores, if available, will not automatically be treated as reliable probabilities. Thresholds must be calibrated against evaluation data.

## 6. Scope

### 6.1 Initial Scope

- Ticket ingestion and validation.
- Structured classification recommendations.
- Priority and routing recommendations.
- Human review and approval.
- Validation of recommended actions.
- Decision and approval audit records.
- Evaluation of classification quality and operational performance.

### 6.2 Initially Out of Scope

- Autonomous customer replies.
- Autonomous refunds, account changes, or other high-impact actions.
- Routing execution without the required approval.
- Replacing the existing ticketing platform.
- Multi-agent architectures without a demonstrated business or technical need.

The final scope requires stakeholder approval.

## 7. Stakeholders

| Stakeholder | Responsibility |
|---|---|
| Support manager | Defines operational objectives, current workflow, KPIs, and SLAs |
| Support agents | Explain practical triage decisions, exceptions, and usability needs |
| Product owner | Establishes scope, priorities, and acceptance criteria |
| IT / platform engineering | Identifies integration capabilities and infrastructure constraints |
| Security / privacy team | Establishes data handling and access-control requirements |
| AI architect | Leads discovery, translates needs into requirements, and documents architecture decisions |

Stakeholder availability and formal ownership must be confirmed.

## 8. Proposed Success Criteria

The following are provisional pilot targets, not approved commitments.

| Metric | Proposed Target | Measurement |
|---|---|---|
| Median triage time | At least 30% reduction | Compare baseline and pilot median times |
| Routing accuracy | At least 95% | Correct assigned team against approved labels |
| Priority agreement | At least 95% | Agreement with validated priority labels |
| Unmodified human acceptance | At least 85% | Recommendations accepted without modification |
| Required approval coverage | 100% | Approved decisions divided by decisions requiring approval |
| Decision traceability | 100% | Decisions with the required audit records |
| Latency | Target to be established | Measure median and p95 processing time |
| Operating cost | Budget to be established | Model and infrastructure cost per processed ticket |

Targets must be reviewed against the actual ticket distribution, business risks, and baseline performance.

Routing and priority metrics should be reported by category and risk level, not just as overall averages. The evaluation dataset must be defined before the pilot to reduce the risk of misleading results.

## 9. Key Risks

| Risk | Potential Impact | Initial Mitigation |
|---|---|---|
| Incorrect classification | Wrong team or delayed resolution | Evaluation datasets, regression tests, and human review |
| Incorrect priority | Urgent tickets may be delayed | Explicit priority policy and deterministic validation |
| Ambiguous ticket content | Unreliable recommendations | Missing-information detection and review escalation |
| Sensitive data exposure | Privacy or compliance incident | Data minimization, access controls, and approved model-provider policies |
| Malicious instructions in tickets | Unauthorized or manipulated behavior | Treat ticket content as untrusted data; constrain tools and permissions |
| Ticketing integration failure | Lost or duplicate actions | Retries, idempotency, audit records, and reconciliation |
| Excessive latency or cost | Reduced operational value | Measure usage, benchmark alternatives, and establish limits |
| Poor human adoption | Limited time savings | Reviewer feedback, usability testing, and acceptance metrics |

These mitigations are initial proposals. Detailed controls will be developed during architecture and security design.

## 10. Discovery Questions

The following questions must be answered or explicitly recorded as unresolved before architecture decisions are finalized.

### Business Workflow

- What is the current triage process?
- What are the median and p95 triage times?
- How many agents participate in triage?
- What are the current routing error and reassignment rates?
- Which service-level agreements must be protected?

### Ticket Data

- Which categories, subcategories, and priority levels exist?
- Are historical tickets labeled with their correct outcomes?
- What languages and ticket formats must be supported?
- How often do tickets lack sufficient information?
- What sensitive information may appear in ticket content?

### Integration and Infrastructure

- Which ticketing platform is used?
- Which APIs, webhooks, and sandbox environments are available?
- What are the expected peak arrival rate and processing latency?
- Which deployment environments are permitted?
- What authentication, authorization, and audit mechanisms already exist?

### Security and Operations

- What data can be sent to an external LLM provider?
- What retention, residency, and deletion requirements apply?
- What availability and recovery objectives are required?
- What operating-cost budget is acceptable?
- Who is responsible for production incidents and model-quality monitoring?

## 11. Architecture Principles

The following principles will guide subsequent design decisions:

1. **Business-first design:** Tie architecture decisions to validated requirements.
2. **Human oversight:** Require authorized approval before executing the corresponding routing action.
3. **Structured outputs:** Validate model results against explicit schemas.
4. **Deterministic controls:** Enforce critical business rules outside the model.
5. **Least privilege:** Limit model and application permissions to necessary operations.
6. **Traceability:** Record recommendations, policy outcomes, approvals, and execution results.
7. **Measurable quality:** Evaluate the system against labeled data and operational baselines.
8. **Incremental complexity:** Start with the simplest architecture that satisfies requirements.
9. **Resilience:** Handle timeouts, malformed outputs, retries, and downstream failures explicitly.

## 12. Discovery Exit Criteria

The Discovery phase is ready to close when:

- [ ] The current triage workflow is documented.
- [ ] Relevant stakeholders have been interviewed.
- [ ] Baseline metrics are measured or their data gaps are recorded.
- [ ] Initial scope and exclusions are reviewed.
- [ ] Ticket categories and routing-policy ownership are identified.
- [ ] Integration and infrastructure constraints are documented.
- [ ] Security and privacy requirements are identified.
- [ ] Success metrics and evaluation methods are agreed upon.
- [ ] Assumptions and open questions have owners and follow-up actions.
- [ ] Stakeholders authorize progression to Requirements Engineering.

## 13. Next Phase

**Phase 02 — Requirements Engineering**

The next phase will transform discovery findings into:

- Business requirements.
- Functional requirements.
- Nonfunctional requirements.
- Ticket taxonomy and routing-policy definitions.
- Use cases and acceptance criteria.
- A prioritized requirements backlog.
- A requirements traceability matrix.

The architecture and technology stack will be selected only after the requirements provide sufficient evidence to justify those decisions.
