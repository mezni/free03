from support_agent.client import chat_with_tools
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.schemas import (
    SEARCH_SIMILAR_TICKETS_TOOL,
)


RESEARCH_SYSTEM_PROMPT = """
You are a customer support research agent.

Your responsibility is to research historical support
tickets that may be similar to the current customer issue.

Use the search_similar_tickets tool when useful.

Do not make decisions about refunds, account changes,
ticket creation, or escalation.

Your job is only to produce research findings.

Return a concise research summary containing:

1. Similar historical cases.
2. Relevant previous resolutions.
3. Useful observations for the support agent.

Do not invent historical cases or resolutions.
"""


def run_research_agent(
    ticket_text: str,
    max_iterations: int = 3,
) -> str:

    messages = [
        {
            "role": "user",
            "content": f"""
Research this customer support issue:

{ticket_text}
""",
        }
    ]

    for _ in range(max_iterations):

        response = chat_with_tools(
            messages=messages,
            tools=[
                SEARCH_SIMILAR_TICKETS_TOOL
            ],
            system=RESEARCH_SYSTEM_PROMPT,
        )

        messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        tool_uses = [
            block
            for block in response.content
            if block.type == "tool_use"
        ]

        if not tool_uses:

            text_blocks = [
                block.text
                for block in response.content
                if block.type == "text"
            ]

            return "\n".join(text_blocks)

        tool_results = []

        for tool_use in tool_uses:

            result = dispatch_tool(
                tool_use.name,
                tool_use.input,
            )

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result.model_dump_json(),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": tool_results,
            }
        )

    raise RuntimeError(
        "Research agent exceeded maximum iterations"
    )