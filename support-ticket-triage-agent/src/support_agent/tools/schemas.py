KNOWLEDGE_BASE_SEARCH_TOOL = {
    "name": "knowledge_base_search",
    "description": (
        "Search the customer support knowledge base for "
        "procedures, troubleshooting instructions, billing "
        "guidance, account guidance, shipping information, "
        "and security procedures. Use this tool when you "
        "need information from the support knowledge base "
        "to answer a customer."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "A concise search query describing the "
                    "customer's issue or the information "
                    "you need to find."
                ),
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}