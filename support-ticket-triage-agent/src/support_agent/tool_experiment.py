from support_agent.client import chat_with_tools
from support_agent.tools.schemas import (
    KNOWLEDGE_BASE_SEARCH_TOOL,
)


def main():
    messages = [
        {
            "role": "user",
            "content": """
A customer says:

My internet has been down since this morning.
I restarted my router several times but it still
does not work.

What should I tell the customer?
""",
        }
    ]

    response = chat_with_tools(
        messages=messages,
        tools=[KNOWLEDGE_BASE_SEARCH_TOOL],
        system="""
You are a customer support assistant.

Use the available tool when you need information
from the support knowledge base.
""",
    )

    for block in response.content:
        print(block)


if __name__ == "__main__":
    main()