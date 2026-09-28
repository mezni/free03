from support_agent.client import chat_with_tools
from support_agent.models.ticket import (
    TicketExtraction,
    TriageDecision,
)
from support_agent.models.tool_result import (
    ToolExecutionResult,
)
from support_agent.tools.dispatcher import dispatch_tool
from support_agent.tools.registry import TOOL_SCHEMAS
from support_agent.memory.conversation import ConversationMemory


SYSTEM_PROMPT = """
You are a customer support agent.

You have been given:

1. The original customer support ticket.
2. Structured ticket information.
3. A triage decision.

Use this information when handling the ticket.

Available tools:

1. knowledge_base_search
2. create_ticket
3. escalate_to_human

Tool reliability rules:

- A tool may fail.
- Check tool results before claiming an action succeeded.
- Do not invent information.
- Do not repeatedly call a failed tool without a reason.

Customer conversation history may be present in the
messages you receive. Use it when relevant.

Provide a professional and helpful response.
"""


def run_agent(
    user_message: str,
    extraction: TicketExtraction,
    triage: TriageDecision,
    memory: ConversationMemory | None = None,
    max_iterations: int = 5,
    max_tool_calls: int = 10,
) -> str:

    if memory is None:
        memory = ConversationMemory()

    context = f"""
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
"""

    memory.add_user_message(context)

    tool_call_count = 0

    for _ in range(max_iterations):

        response = chat_with_tools(
            messages=memory.get_messages(),
            tools=TOOL_SCHEMAS,
            system=SYSTEM_PROMPT,
        )

        memory.add_assistant_message(
            response.content
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

            tool_call_count += 1

            if tool_call_count >= max_tool_calls:
                raise RuntimeError(
                    "Agent exceeded maximum tool calls"
                )

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

        memory.add_message(
            "user",
            tool_results,
        )

    raise RuntimeError(
        "Agent exceeded maximum iterations"
    )