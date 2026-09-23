import json
import re


def parse_json(raw_result: str) -> dict:
    text = raw_result.strip()

    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)

    return json.loads(text)