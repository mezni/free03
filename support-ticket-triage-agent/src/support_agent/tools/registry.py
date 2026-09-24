from support_agent.tools.knowledge_base import (
    knowledge_base_search,
)
from support_agent.tools.schemas import (
    KNOWLEDGE_BASE_SEARCH_TOOL,
)


TOOL_FUNCTIONS = {
    "knowledge_base_search": knowledge_base_search,
}


TOOL_SCHEMAS = [
    KNOWLEDGE_BASE_SEARCH_TOOL,
]