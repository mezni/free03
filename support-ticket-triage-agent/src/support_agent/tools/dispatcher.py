from typing import Any, Set

from support_agent.models.tool_result import (
    ToolExecutionResult,
)
from support_agent.tools.registry import TOOL_FUNCTIONS


READ_ONLY_TOOLS: Set[str] = {
    "knowledge_base_search",
    "search_similar_tickets",
}

STATE_CHANGING_TOOLS: Set[str] = {
    "create_ticket",
    "escalate_to_human",
}


def dispatch_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    allowed_tools: set | None = None,
) -> ToolExecutionResult:

    if allowed_tools is not None and tool_name not in allowed_tools:
        return ToolExecutionResult(
            success=False,
            error=f"Tool {tool_name} is not allowed in this context",
            error_type="UnauthorizedTool",
        )

    tool = TOOL_FUNCTIONS.get(tool_name)

    if tool is None:
        return ToolExecutionResult(
            success=False,
            error=f"Unknown tool: {tool_name}",
            error_type="UnknownTool",
        )

    try:
        result = tool(**tool_input)

        return ToolExecutionResult(
            success=True,
            data=result,
        )

    except Exception as exc:
        return ToolExecutionResult(
            success=False,
            error=str(exc),
            error_type=type(exc).__name__,
        )