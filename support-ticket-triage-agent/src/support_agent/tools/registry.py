from support_agent.tools.escalation import (
    escalate_to_human,
)
from support_agent.tools.historical_tickets import (
    search_similar_tickets,
)
from support_agent.tools.knowledge_base import (
    knowledge_base_search,
)
from support_agent.tools.ticketing import (
    create_ticket,
)
from support_agent.tools.schemas import (
    KNOWLEDGE_BASE_SEARCH_TOOL,
    CREATE_TICKET_TOOL,
    ESCALATE_TO_HUMAN_TOOL,
    SEARCH_SIMILAR_TICKETS_TOOL,
)


TOOL_FUNCTIONS = {
    "knowledge_base_search": knowledge_base_search,
    "create_ticket": create_ticket,
    "escalate_to_human": escalate_to_human,
    "search_similar_tickets": search_similar_tickets,
}


TOOL_SCHEMAS = [
    KNOWLEDGE_BASE_SEARCH_TOOL,
    CREATE_TICKET_TOOL,
    ESCALATE_TO_HUMAN_TOOL,
    SEARCH_SIMILAR_TICKETS_TOOL,
]