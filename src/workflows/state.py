# src/workflows/state.py
import operator
from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    # Appends new messages automatically to the ongoing conversation list
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Stores the routing decision returned by the supervisor
    next_agent: str
