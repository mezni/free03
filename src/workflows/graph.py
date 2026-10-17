# src/workflows/graph.py
from langgraph.graph import END, START, StateGraph

from src.agents.researcher import researcher_node
from src.agents.supervisor import supervisor_node
from src.agents.writer import writer_node
from src.workflows.state import AgentState


def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Writer", writer_node)

    # 2. Set entry point
    workflow.add_edge(START, "Supervisor")

    # 3. Conditional routing from Supervisor
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
