from langchain_openrouter import ChatOpenRouter

from triage_ai.config import settings


def create_chat_model() -> ChatOpenRouter:
    return ChatOpenRouter(
        model=settings.openrouter_model,
        api_key=settings.openrouter_api_key,
    )