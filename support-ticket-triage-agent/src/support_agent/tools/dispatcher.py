from typing import Any

from support_agent.models.tool_result import (
    ToolExecutionResult,
)
from support_agent.tools.registry import TOOL_FUNCTIONS


def dispatch_tool(
    tool_name: str,
    tool_input: dict[str, Any],
) -> ToolExecutionResult:

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