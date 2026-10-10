# Stakeholder Interview Guide — AI Ticket Triage

| Field | Value |
|---|---|
| Project | `ticket-triage` |
| Phase | 01 — Discovery |
| Document status | Draft — interviews pending |
| Owner | AI Architect |
| Primary objective | Reduce manual ticket triage time |
| Proposed operating model | AI recommendation followed by human approval |

---

## 1. Purpose

The purpose of stakeholder interviews is to understand the current ticket triage process, identify business problems, establish measurable success criteria, and discover constraints that will influence the AI system architecture.

The interviews must establish what the system needs to achieve before selecting an LLM provider, agent framework, database, or deployment platform.

## 2. Stakeholder Map

| Stakeholder | Information Required | Expected Output |
|---|---|---|
| Support manager | Workflow, volume, KPIs, SLAs, bottlenecks | Business baseline and objectives |
| Support agents | Classification decisions, exceptions, usability | Representative cases and workflow requirements |
| Product owner | Scope, priorities, acceptance criteria | Prioritized business needs |
| IT / platform engineer | APIs, integrations, infrastructure, reliability | Integration and technical constraints |
| Security / privacy representative | Data classification, access, retention, compliance | Security and privacy requirements |

Stakeholder names, availability, and ownership are not yet confirmed.

## 3. Interview Procedure

Use the following process for each interview.

1. Explain the purpose of the project and the interview.
2. Ask the stakeholder to describe the existing process without proposing a solution.
3. Collect concrete examples, measurements, and supporting evidence.
4. Identify exceptions, failure scenarios, and operational constraints.
5. Clarify ambiguous statements with follow-up questions.
6. Separate confirmed facts from assumptions and opinions.
7. Summarize findings and ask the stakeholder to validate your interpretation.
8. Record follow-up actions, owners, and deadlines.

Do not treat a stakeholder's desired solution as a confirmed requirement until the underlying business need is understood.

---

## 4. Interview A — Support Manager

**Duration:** 45 minutes

**Objective:** Understand the operational workflow and establish the business baseline.

### Questions

#### Current Workflow

1. Walk me through the lifecycle of a ticket from arrival to assignment.
2. Which steps require a human to read, classify, prioritize, or route the ticket?
3. Which teams participate in the process?
4. What happens when a ticket is assigned to the wrong team?
5. Which steps create the most delay or rework?

#### Volume and Performance

6. How many tickets arrive on an average day?
7. What are the peak daily and hourly volumes?
8. What are the median and 95th-percentile triage times?
9. What proportion of tickets are reassigned?
10. How is routing accuracy measured today?
11. Which SLAs or escalation deadlines must be protected?

#### Business Priorities

12. Which ticket categories consume the most triage effort?
13. Which errors have the greatest operational impact?
14. What improvement would justify a pilot?
15. Which decisions must always remain under human control?

### Evidence to Collect

- Existing workflow documentation.
- Operational dashboards and reports.
- Current triage-time measurements.
- Routing and reassignment statistics.
- Ticket category and priority definitions.
- SLA and escalation policies.

### Interview Output

Document the current workflow, baseline metrics, primary pain points, and agreed business objectives.

---

## 5. Interview B — Frontline Support Agents

**Duration:** 30–45 minutes

**Objective:** Understand the practical decisions agents make and identify cases that require human judgment.

### Questions

1. What information do you inspect before assigning a ticket?
2. Which categories are most difficult to distinguish?
3. How do you determine priority?
4. Which tickets frequently lack enough information?
5. What causes you to reassign a ticket?
6. Which ticket types require specialist knowledge?
7. What makes a recommendation useful and trustworthy?
8. What evidence would you need to approve an AI recommendation?
9. How should you correct a wrong recommendation?
10. Which cases should always be escalated?

### Practical Exercise

Ask the agent to walk through three to five anonymized tickets:

- A straightforward ticket.
- An ambiguous ticket.
- A high-priority or unusual ticket.

For each example, record the expected category, priority, destination team, rationale, and any information needed before taking action.

### Evidence to Collect

- Representative anonymized tickets.
- Examples of classification disagreements.
- Common missing-information patterns.
- Reassignment and escalation examples.
- Reviewer feedback and usability expectations.

### Interview Output

Create a collection of representative ticket scenarios and expected outcomes for requirements definition and future evaluation.

---

## 6. Interview C — Product Owner

**Duration:** 30 minutes

**Objective:** Define the minimum viable product, project boundaries, and acceptance criteria.

### Questions

1. Which business outcomes are most important?
2. Which ticket categories must the first version support?
3. Which ticket channels are in scope?
4. What must the first release do?
5. What is explicitly out of scope?
6. Who approves recommendations?
7. May the system execute an approved routing action automatically?
8. What happens when a recommendation is rejected?
9. Which metrics determine pilot acceptance?
10. Who signs off on requirements and release readiness?

### Evidence to Collect

- Product objectives and roadmap.
- Initial feature priorities.
- Business acceptance criteria.
- Scope exclusions.
- Stakeholder approval responsibilities.

### Interview Output

Produce a prioritized initial scope and a set of proposed acceptance criteria for stakeholder review.

---

## 7. Interview D — IT and Platform Engineering

**Duration:** 45 minutes

**Objective:** Discover integration capabilities, infrastructure constraints, and reliability requirements.

### Questions

#### Existing Systems

1. Which ticketing platform and version are currently used?
2. Are APIs, webhooks, and sandbox environments available?
3. How are tickets authenticated and authorized?
4. Are there API rate limits or integration restrictions?
5. Can the system subscribe to ticket events?

#### Workload and Performance

6. What peak ticket arrival rate must be supported?
7. What is the acceptable time to produce a recommendation?
8. Must processing be synchronous or asynchronous?
9. What availability and recovery objectives apply?
10. How should duplicate events and failed updates be handled?

#### Infrastructure

11. Which cloud or on-premises environments are permitted?
12. What database and messaging services are available?
13. Are there approved LLM providers or model-hosting restrictions?
14. How are secrets, service accounts, and environment configuration managed?
15. Which monitoring and deployment tools are already in use?

### Evidence to Collect

- API documentation.
- Integration diagrams.
- Sandbox access requirements.
- Infrastructure standards.
- Capacity and availability requirements.
- Authentication and authorization standards.

### Interview Output

Create an integration inventory, preliminary deployment constraints, and a list of technical dependencies.

---

## 8. Interview E — Security and Privacy

**Duration:** 30–45 minutes

**Objective:** Establish permitted data handling, access controls, auditability, and security risks.

### Questions

1. What types of sensitive data may appear in ticket content?
2. Which data may be sent to an external LLM provider?
3. What data residency and retention policies apply?
4. Which roles may view tickets and approve recommendations?
5. What audit records must be retained?
6. How must the system protect personal information in logs?
7. How should the system handle malicious instructions embedded in ticket content?
8. What controls prevent the model from performing unauthorized actions?
9. What security reviews or assessments are required before deployment?
10. What incident-response process applies to a data exposure or incorrect routing event?

### Evidence to Collect

- Data classification policies.
- Approved model-provider requirements.
- Access-control standards.
- Retention and deletion requirements.
- Audit and incident-response policies.
- Applicable compliance obligations.

### Interview Output

Document data-handling restrictions, security requirements, initial threat scenarios, and outstanding compliance questions.

---

## 9. Interview Notes Template

Complete this section immediately after each interview.

### Interview Metadata

- **Stakeholder:**
- **Role:**
- **Date:**
- **Interviewer:**
- **Duration:**

### A. Confirmed Facts

Record statements supported by evidence or explicitly confirmed by the stakeholder.

- 
- 
- 

### B. Business Needs

Record the underlying problems and desired outcomes.

- 
- 
- 

### C. Requirements Candidates

Record potential requirements that still need formal definition.

- 
- 
- 

### D. Assumptions

Record statements that have not been verified.

- 
- 
- 

### E. Constraints and Risks

Record technical, operational, security, and business constraints.

- 
- 
- 

### F. Open Questions

| Question | Why It Matters | Owner | Due Date |
|---|---|---|---|
| | | | |

### G. Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| | | | Open |

### H. Stakeholder Validation

- Summary shared with stakeholder: Yes / No
- Corrections received:
- Outstanding disagreements:
- Follow-up meeting required: Yes / No

---

## 10. Requirements Traceability

Every important discovery finding should eventually connect to a requirement, an implementation decision, and a test.

| Finding ID | Discovery Finding | Requirement ID | Architecture Decision | Validation |
|---|---|---|---|---|
| FIND-001 | To be established | TBD | TBD | TBD |
| FIND-002 | To be established | TBD | TBD | TBD |
| FIND-003 | To be established | TBD | TBD | TBD |

Do not invent findings to fill this table. Populate it as evidence becomes available.

## 11. Discovery Completion Criteria

The interview phase is ready to close when:

- [ ] The support manager's workflow and baseline data have been documented.
- [ ] Frontline agents have provided representative ticket examples.
- [ ] The product owner has reviewed the initial scope.
- [ ] IT has documented integration capabilities and constraints.
- [ ] Security and privacy requirements have been identified.
- [ ] Assumptions and open questions have owners.
- [ ] Conflicting stakeholder expectations have been recorded.
- [ ] Findings have been translated into candidate requirements.
- [ ] Stakeholders have reviewed the discovery summary.

## 12. Next Step

**Proceed to Phase 02 — Requirements Engineering.**

Use the interview findings to create:

- Business requirements.
- Functional requirements.
- Nonfunctional requirements.
- Ticket taxonomy and routing-policy definitions.
- Use cases and acceptance criteria.
- A prioritized requirements backlog.
- A requirements traceability matrix.

Architecture decisions should be based on validated requirements and documented trade-offs rather than assumptions made during initial discovery.
