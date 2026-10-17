# src/tools/search.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

search_run = DuckDuckGoSearchRun()


@tool("web_search")
def web_search_tool(query: str) -> str:
    """Search the web for up-to-date facts, news, and technical documentation."""
    try:
        return search_run.run(query)
    except Exception as e:
        return f"Error executing search: {str(e)}"
