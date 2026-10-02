from dataclasses import dataclass, field


@dataclass
class ConversationMemory:
    messages: list[dict] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )

    def add_assistant_message(self, content) -> None:
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
            }
        )

    def add_tool_result(self, content) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )

    def get_messages(self) -> list[dict]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()