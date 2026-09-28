import json
import re


class GuardrailViolation(Exception):
    """Raised when an agent violates an application rule."""


def validate_extraction_output(
    raw_response: str,
) -> "TicketExtraction":

    text = raw_response.strip()

    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)

    try:
        data = json.loads(text)

    except json.JSONDecodeError as exc:
        raise GuardrailViolation(
            "Extraction model returned invalid JSON"
        ) from exc

    try:
        from support_agent.models.ticket import TicketExtraction

        return TicketExtraction.model_validate(data)

    except Exception as exc:
        raise GuardrailViolation(
            "Extraction output failed schema validation"
        ) from exc


def validate_triage_output(
    raw_response: str,
) -> "TriageDecision":

    import json

    from support_agent.models.ticket import TriageDecision

    text = raw_response.strip()

    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)

    try:
        data = json.loads(text)

    except json.JSONDecodeError as exc:
        raise GuardrailViolation(
            "Triage model returned invalid JSON"
        ) from exc

    try:
        return TriageDecision.model_validate(data)

    except Exception as exc:
        raise GuardrailViolation(
            "Triage output failed schema validation"
        ) from exc


def validate_triage_decision(
    decision: "TriageDecision",
) -> "TriageDecision":

    if (
        decision.category == "security"
        and not decision.needs_escalation
    ):
        raise GuardrailViolation(
            "Security tickets must be escalated."
        )

    return decision


def validate_escalation(
    priority: str,
    reason: str,
) -> None:

    if priority not in {
        "high",
        "critical",
    }:
        raise GuardrailViolation(
            "Escalation requires high or critical priority."
        )

    if not reason.strip():
        raise GuardrailViolation(
            "Escalation requires a reason."
        )