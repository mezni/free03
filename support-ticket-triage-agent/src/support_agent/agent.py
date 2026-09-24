from support_agent.client import chat_with_tools
from support_agent.models.ticket import (
    TicketExtraction,
    TriageDecision,
)
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.registry import TOOL_SCHEMAS


def run_agent(
    user_message: str,
    extraction: TicketExtraction,
    triage: TriageDecision,
    max_iterations: int = 5,
) -> str:

    messages = [
        {
            "role": "user",
            "content": f"""
Customer support ticket:

{user_message}

Structured ticket information:

Customer ID:
{extraction.customer_id}

Product:
{extraction.product}

Sentiment:
{extraction.sentiment}

Priority:
{extraction.priority}

Triage decision:

Category:
{triage.category}

Urgency:
{triage.urgency}

Needs knowledge search:
{triage.needs_knowledge_search}

Needs escalation:
{triage.needs_escalation}
""",
        }
    ]

    for _ in range(max_iterations):

        response = chat_with_tools(
            messages=messages,
            tools=TOOL_SCHEMAS,
            system="""
You are a customer support agent.

You have been given:

1. The original customer support ticket.
2. Structured ticket information.
3. A triage decision.

Use this information when handling the ticket.

Use available tools when they are necessary.

Do not invent company policies, account changes,
refunds, or actions that have not been provided
by the available tools or knowledge base.

Provide a professional and helpful response.
""",
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

            print(
                f"\n[AGENT] Tool requested: "
                f"{tool_use.name}"
            )

            print(
                f"[AGENT] Input: "
                f"{tool_use.input}"
            )

            result = dispatch_tool(
                tool_use.name,
                tool_use.input,
            )

            print(
                f"[AGENT] Result: "
                f"{result}"
            )

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": tool_results,
            }
        )

    raise RuntimeError(
        "Agent exceeded maximum iterations"
    )