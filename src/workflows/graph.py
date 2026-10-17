# src/workflows/graph.py
from langgraph.graph import END, START, StateGraph

from src.agents.supervisor import supervisor_node
from src.workflows.state import AgentState


# Temporary placeholders (will be replaced in Phase 3)
def researcher_placeholder(state: AgentState):
    return {"messages": [("assistant", "[Researcher]: Gathering mock data...")]}


def writer_placeholder(state: AgentState):
    return {"messages": [("assistant", "[Writer]: Drafting mock summary...")]}


def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Researcher", researcher_placeholder)
    workflow.add_node("Writer", writer_placeholder)

    # 2. Set entry point
    workflow.add_edge(START, "Supervisor")

    # 3. Add conditional routing from Supervisor
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next_agent"],
        {"Researcher": "Researcher", "Writer": "Writer", "FINISH": END},
    )

    # 4. Workers report back to the Supervisor
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Writer", "Supervisor")

    return workflow.compile()


graph = build_graph()
