from support_agent.models.handoff import ResearchRequest
from support_agent.models.ticket import (
    SupportTicket,
    TicketExtraction,
    TriageDecision,
)
from support_agent.research_agent import (
    run_research_agent,
)


def build_research_request(
    ticket: SupportTicket,
    extraction: TicketExtraction,
    triage: TriageDecision,
) -> ResearchRequest:

    return ResearchRequest(
        ticket_id=ticket.ticket_id,
        customer_id=extraction.customer_id,
        issue_summary=(
            f"{ticket.subject}: {ticket.body}"
        ),
        category=triage.category,
        urgency=triage.urgency,
        product=extraction.product,
        priority=extraction.priority,
        research_question=(
            "Find historical support cases similar "
            "to this customer issue and identify "
            "previous resolutions."
        ),
    )


def research_ticket(
    ticket: SupportTicket,
    extraction: TicketExtraction,
    triage: TriageDecision,
):

    request = build_research_request(
        ticket=ticket,
        extraction=extraction,
        triage=triage,
    )

    return run_research_agent(request)