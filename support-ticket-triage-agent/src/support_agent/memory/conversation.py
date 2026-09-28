from dataclasses import dataclass, field


@dataclass
class ConversationMemory:
    messages: list[dict] = field(default_factory=list)

    def add_user_message(
        self,
        content: str,
    ) -> None:
        self.add_message(
            "user",
            content,
        )

    def add_assistant_message(
        self,
        content,
    ) -> None:
        self.add_message(
            "assistant",
            content,
        )

    def add_message(
        self,
        role: str,
        content,
    ) -> None:
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(self) -> list[dict]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()