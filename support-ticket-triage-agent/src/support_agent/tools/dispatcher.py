from typing import Any

from support_agent.tools.registry import TOOL_FUNCTIONS


def dispatch_tool(
    tool_name: str,
    tool_input: dict[str, Any],
) -> Any:

    tool = TOOL_FUNCTIONS.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    return tool(**tool_input)