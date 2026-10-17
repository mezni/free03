# src/agents/researcher.py
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.tools.search import web_search_tool
from src.workflows.state import AgentState


def researcher_node(state: AgentState):
    tools = [web_search_tool]
    llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

    researcher_prompt = (
        "You are an expert technical researcher. Your goal is to gather accurate facts "
        "and details relevant to the user's request. Use the 'web_search' tool when you need "
        "external data. Focus purely on accurate facts and raw information."
    )

    messages = [SystemMessage(content=researcher_prompt)] + list(state["messages"])
    response = llm.invoke(messages)

    output_messages = [response]
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "web_search":
                tool_output = web_search_tool.invoke(tool_call["args"])
                output_messages.append(
                    ToolMessage(
                        content=tool_output,
                        tool_call_id=tool_call["id"],
                        name="web_search",
                    )
                )

    return {"messages": output_messages}
