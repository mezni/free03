# src/agents/writer.py
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.workflows.state import AgentState

llm = ChatOpenAI(model="gpt-4o", temperature=0)


def writer_node(state: AgentState):
    writer_prompt = (
        "You are an expert technical writer. Take the research notes and findings "
        "provided in the conversation and synthesize them into a clean, professional, "
        "and well-structured markdown report for the user."
    )

    messages = [SystemMessage(content=writer_prompt)] + list(state["messages"])
    response = llm.invoke(messages)

    return {"messages": [HumanMessage(content=response.content, name="Writer")]}
