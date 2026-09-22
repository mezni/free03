from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

client = Anthropic()

MODEL = "claude-haiku-4-5-20251001"


def chat(messages: list[dict], system: str | None = None) -> str:
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    response = client.messages.create(**params)

    return response.content[0].text