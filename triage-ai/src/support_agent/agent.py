from support_agent.memory import ConversationMemory
from support_agent.memory_service import MemoryService
from support_agent.prompts import build_triage_system_prompt


class SupportAgent:

    def __init__(
        self,
        max_turns: int = 5,
        memory_service: MemoryService | None = None,
    ):
        self.max_turns = max_turns
        self.memory_service = memory_service or MemoryService()
        self.memory = ConversationMemory()

    def run(
        self,
        user_message: str,
        customer_id: str | None = None,
    ):

        memory_context = None

        if customer_id:
            self.memory_service.process_message(
                user_message
            )

            memory_context = self.memory_service.get_context(
                customer_id=customer_id,
                query=user_message,
            )

        system_prompt = build_triage_system_prompt(
            memory_context=memory_context,
        )

        messages = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        response = self._call_llm(
            system_prompt=system_prompt,
            messages=messages,
        )

        self.memory.add_user_message(user_message)

        self.memory.messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_result = self._execute_tool(tool_call)
                self.memory.messages.append(
                    {
                        "role": "user",
                        "content": tool_result,
                    }
                )

        return response

    def _call_llm(self, system_prompt, messages, tools=None):
        raise NotImplementedError("Subclasses must implement _call_llm")

    def _execute_tool(self, tool_call):
        raise NotImplementedError("Subclasses must implement _execute_tool")
