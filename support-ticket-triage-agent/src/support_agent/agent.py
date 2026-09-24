from support_agent.client import chat_with_tools
from support_agent.models.ticket import (
    TicketExtraction,
    TriageDecision,
)
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.schemas import (
    KNOWLEDGE_BASE_SEARCH_TOOL,
)


TOOLS = [
    KNOWLEDGE_BASE_SEARCH_TOOL,
]


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
            tools=TOOLS,
            system="""
You are a customer support agent.

You have been given:

1. The original customer support ticket.
2. Structured ticket information.
3. A triage decision.

Use this information when handling the ticket.

You may use the knowledge base search tool when
additional support information is required.

If the triage decision indicates that escalation
is required, do not attempt to resolve the issue
without appropriate human involvement.

Do not invent company policies, refunds, account
changes, or other actions that have not been
provided by the available tools or knowledge base.

Provide a professional and helpful response.

Follow the triage decision.

If needs_knowledge_search is false, do not use
the knowledge base search unless the ticket cannot
be handled safely without it.

If needs_escalation is true, the case requires
human escalation and should not be presented as
fully resolved by the AI.
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