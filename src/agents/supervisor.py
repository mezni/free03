# src/agents/supervisor.py
from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.workflows.state import AgentState


class RouterResponse(BaseModel):
    next_agent: Literal["Researcher", "Writer", "FINISH"]


def supervisor_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    supervisor_prompt = (
        "You are a supervisor managing a team of two specialized agents:\n"
        "1. 'Researcher': Gathers facts, data, and information.\n"
        "2. 'Writer': Synthesizes research into a structured response.\n\n"
        "Review the conversation history and decide the next step:\n"
        "- Delegate to 'Researcher' if information is missing or needs gathering.\n"
        "- Delegate to 'Writer' if research is complete and needs formatting.\n"
        "- Respond with 'FINISH' if the task is fully completed and answered."
    )

    messages = [SystemMessage(content=supervisor_prompt)] + list(state["messages"])
    structured_llm = llm.with_structured_output(RouterResponse)
    result = structured_llm.invoke(messages)

    return {"next_agent": result.next_agent}
