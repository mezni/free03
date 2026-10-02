import json

from pydantic import ValidationError

from support_agent.llm import call_llm
from support_agent.models import MemoryExtractionResult
from support_agent.prompts import (
    MEMORY_EXTRACTION_SYSTEM_PROMPT,
)


class MemoryExtractionError(Exception):
    pass


def extract_memory_candidates(
    message: str,
) -> MemoryExtractionResult:

    response = call_llm(
        system_prompt=MEMORY_EXTRACTION_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    text = next(
        block.text
        for block in response.content
        if block.type == "text"
    )

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MemoryExtractionError(
            "LLM returned invalid JSON."
        ) from exc

    try:
        return MemoryExtractionResult.model_validate(data)
    except ValidationError as exc:
        raise MemoryExtractionError(
            "LLM returned invalid memory data."
        ) from exc