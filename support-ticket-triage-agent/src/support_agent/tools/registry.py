from support_agent.tools.escalation import (
    escalate_to_human,
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
)


TOOL_FUNCTIONS = {
    "knowledge_base_search": knowledge_base_search,
    "create_ticket": create_ticket,
    "escalate_to_human": escalate_to_human,
}


TOOL_SCHEMAS = [
    KNOWLEDGE_BASE_SEARCH_TOOL,
    CREATE_TICKET_TOOL,
    ESCALATE_TO_HUMAN_TOOL,
]