from support_agent.client import chat_with_tools
from support_agent.models.handoff import (
    ResearchRequest,
    ResearchResult,
)
from support_agent.models.research import SimilarTicket
from support_agent.tools.agent_tools import (
    RESEARCH_AGENT_TOOLS,
)
from support_agent.tools.dispatcher import dispatch_tool


RESEARCH_SYSTEM_PROMPT = """
You are a customer support research agent.

Your responsibility is to research historical support
tickets that may be similar to the current customer issue.

You have exactly one capability:

- search_similar_tickets

You must not:
- create tickets
- escalate customers
- modify customer accounts
- make support decisions
- promise refunds

Your job is to provide research findings to another
support agent.

Do not invent historical cases or resolutions.
"""


def run_research_agent(
    request: ResearchRequest,
    max_iterations: int = 3,
) -> ResearchResult:

    messages = [
        {
            "role": "user",
            "content": f"""
Research this support case.

Ticket ID:
{request.ticket_id}

Customer ID:
{request.customer_id}

Issue:
{request.issue_summary}

Category:
{request.category}

Urgency:
{request.urgency}

Product:
{request.product}

Priority:
{request.priority}

Research question:
{request.research_question}
""",
        }
    ]

    for _ in range(max_iterations):

        response = chat_with_tools(
            messages=messages,
            tools=RESEARCH_AGENT_TOOLS,
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

            findings = "\n".join(text_blocks)

            return ResearchResult(
                ticket_id=request.ticket_id,
                findings=findings,
                similar_tickets=[],
            )

        tool_results = []

        for tool_use in tool_uses:

            result = dispatch_tool(
                tool_use.name,
                tool_use.input,
                allowed_tools={
                    "search_similar_tickets",
                },
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