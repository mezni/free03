# src/workflows/graph.py
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from src.agents.researcher import researcher_node
from src.agents.supervisor import supervisor_node
from src.agents.writer import writer_node
from src.workflows.state import AgentState

# Open a persistent SQLite connection for LangGraph checkpointing
sqlite_conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)


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

    # Compile graph with the persistent checkpointer
    return workflow.compile(checkpointer=memory)


graph = build_graph()
