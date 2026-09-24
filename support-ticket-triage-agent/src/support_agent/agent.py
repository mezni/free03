from support_agent.client import chat_with_tools
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.schemas import (
    KNOWLEDGE_BASE_SEARCH_TOOL,
)


TOOLS = [
    KNOWLEDGE_BASE_SEARCH_TOOL,
]


def run_agent(
    user_message: str,
    max_iterations: int = 5,
) -> str:
    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    for _ in range(max_iterations):
        response = chat_with_tools(
            messages=messages,
            tools=TOOLS,
            system="""
You are a customer support assistant.

Use the knowledge base search tool when you need
support procedures or troubleshooting information.

After obtaining the necessary information, provide
a helpful response to the customer.

Do not invent company policies.
""",
        )

        messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        for block in response.content:

            if block.type == "text":
                return block.text

            if block.type == "tool_use":

                tool_result = dispatch_tool(
                    block.name,
                    block.input,
                )

                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(tool_result),
                            }
                        ],
                    }
                )

    raise RuntimeError(
        "Agent exceeded maximum iterations"
    )