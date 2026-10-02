from dataclasses import dataclass, field


@dataclass
class AgentState:
    customer_id: str | None = None
    category: str | None = None
    priority: str | None = None
    product: str | None = None
    ticket_id: str | None = None

    tool_results: list[str] = field(
        default_factory=list
    )


from support_agent.models import ExtractedTicket


def update_state_from_extraction(
    state: AgentState,
    extracted: ExtractedTicket,
) -> None:

    state.customer_id = extracted.customer_id
    state.product = extracted.product
    state.category = (
        extracted.category.value
        if hasattr(extracted.category, "value")
        else extracted.category
    )
    state.priority = (
        extracted.priority.value
        if hasattr(extracted.priority, "value")
        else extracted.priority
    )