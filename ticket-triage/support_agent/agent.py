import json
import os
from enum import Enum

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel


def get_customer_status(customer_id: str) -> str:
    customers = {
        "C001": "active",
        "C002": "active",
        "C003": "suspended",
    }

    return customers.get(customer_id, "unknown")


CUSTOMER_STATUS_TOOL = {
    "name": "get_customer_status",
    "description": (
        "Get the current account status of a customer. "
        "Use this when you need to verify whether a customer "
        "account is active, suspended, or unknown."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The unique customer identifier.",
            }
        },
        "required": ["customer_id"],
    },
}

TOOL_SCHEMAS = [
    CUSTOMER_STATUS_TOOL,
]

TOOL_REGISTRY = {
    "get_customer_status": get_customer_status,
}


class SupportAgent:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns

    def run(self, user_message: str):
        messages = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        for turn in range(self.max_turns):
            response = call_llm(
                system_prompt=TRIAGE_SYSTEM_PROMPT,
                messages=messages,
                tools=TOOL_SCHEMAS,
            )

            print(f"\n--- Turn {turn + 1} ---")
            print("Stop reason:", response.stop_reason)

            if response.stop_reason == "end_turn":
                return response

            if response.stop_reason == "tool_use":
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                    }
                )

                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    result = self._execute_tool(
                        block.name,
                        block.input,
                    )

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

                messages.append(
                    {
                        "role": "user",
                        "content": tool_results,
                    }
                )

                continue

            raise RuntimeError(f"Unexpected stop reason: {response.stop_reason}")

        raise RuntimeError("Agent exceeded maximum number of turns.")

    def _execute_tool(self, name: str, arguments: dict) -> str:
        tool = TOOL_REGISTRY.get(name)

        if tool is None:
            return f"Unknown tool: {name}"

        try:
            result = tool(**arguments)
            return str(result)
        except Exception as exc:
            return f"Tool execution failed: {exc}"


class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    message: str


class TicketCategory(str, Enum):
    ACCOUNT = "account"
    BILLING = "billing"
    TECHNICAL = "technical"
    PRODUCT = "product"
    SHIPPING = "shipping"
    OTHER = "other"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TriageResult(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    reasoning: str
    response: str


load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv(
    "ANTHROPIC_MODEL",
    "claude-sonnet-4-6",
)

if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not configured.")


TRIAGE_SYSTEM_PROMPT = """
You are a customer support triage assistant.

Your job is to analyze a customer support ticket.

You can use available tools when additional information
is required.

Available capability:

- get_customer_status: retrieve the current status of a customer account.

Use a tool when it provides information necessary to make
a better decision.

Do not claim that you performed an action that you did not perform.

Do not invent information.

When you have enough information, provide a final response
to the customer.
"""

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def call_llm(
    *,
    system_prompt: str,
    messages: list[dict],
    tools: list[dict] | None = None,
):
    kwargs = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": messages,
    }

    if tools:
        kwargs["tools"] = tools

    return client.messages.create(**kwargs)


def _extract_json(raw_response: str) -> dict:
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json") :]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(cleaned[start : end + 1])

    raise ValueError(f"Could not parse LLM response as JSON: {raw_response!r}")


def triage_ticket(ticket: SupportTicket) -> TriageResult:
    raw_response = ask_llm(
        system_prompt=TRIAGE_SYSTEM_PROMPT,
        user_message=ticket.message,
    )

    data = _extract_json(raw_response)

    return TriageResult.model_validate(data)
