# app.py
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from src.workflows.graph import graph

load_dotenv()

st.set_page_config(
    page_title="relay-agent | Multi-Agent Workspace",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 relay-agent Workspace")
st.caption("A modular multi-agent supervisor system powered by LangGraph & GPT-4o.")

# Check for API Key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API key not found. Please check your `.env` file.")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt input box
if prompt := st.chat_input("What would you like the agents to research or write?"):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Execute workflow graph with live status updates
    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        response_placeholder = st.empty()

        initial_state = {
            "messages": [HumanMessage(content=prompt)],
            "next_agent": "Supervisor",
        }

        final_response = ""

        try:
            with st.status(
                "⚡ Running multi-agent workflow...", expanded=True
            ) as status:
                for event in graph.stream(initial_state):
                    for node_name, output in event.items():
                        st.write(f"🔄 **Node Executed:** `{node_name}`")
                        if "next_agent" in output:
                            st.write(
                                f"🎯 **Routing Decision:** `{output['next_agent']}`"
                            )
                        if "messages" in output:
                            for msg in output["messages"]:
                                if hasattr(msg, "tool_calls") and msg.tool_calls:
                                    for call in msg.tool_calls:
                                        st.write(f"🛠️ *Tool Called:* `{call['name']}`")
                                elif isinstance(msg, ToolMessage):
                                    st.write("📥 *Fetched live web data*")
                                elif isinstance(msg, AIMessage) and msg.content:
                                    final_response = msg.content
                status.update(
                    label="✅ Workflow Execution Complete!",
                    state="complete",
                    expanded=False,
                )

            # Fallback if final response wasn't caught in stream loop
            if not final_response:
                final_response = "Task completed successfully, but no direct text output was generated."

            response_placeholder.markdown(final_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_response}
            )

        except Exception as e:
            error_msg = f"❌ Error during execution: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )
