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


CREATE_TICKET_TOOL = {
    "name": "create_ticket",
    "description": (
        "Create a new customer support ticket when a "
        "follow-up case needs to be recorded for support "
        "handling. Use the customer's existing customer ID. "
        "Do not create duplicate tickets for the same issue."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": (
                    "The customer ID from the support ticket."
                ),
            },
            "subject": {
                "type": "string",
                "description": (
                    "A concise subject describing the "
                    "support issue."
                ),
            },
            "description": {
                "type": "string",
                "description": (
                    "A clear description of the issue "
                    "that should be recorded in the new ticket."
                ),
            },
            "priority": {
                "type": "string",
                "enum": [
                    "low",
                    "medium",
                    "high",
                    "critical",
                ],
                "description": (
                    "The priority assigned to the new ticket."
                ),
            },
        },
        "required": [
            "customer_id",
            "subject",
            "description",
            "priority",
        ],
        "additionalProperties": False,
    },
}


ESCALATE_TO_HUMAN_TOOL = {
    "name": "escalate_to_human",
    "description": (
        "Escalate a customer support case to a human "
        "support agent when the issue requires human "
        "intervention. Provide the ticket ID, a concise "
        "reason for escalation, and the appropriate priority."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ticket_id": {
                "type": "string",
                "description": (
                    "The ID of the customer support ticket "
                    "being escalated."
                ),
            },
            "reason": {
                "type": "string",
                "description": (
                    "A concise explanation of why human "
                    "support intervention is required."
                ),
            },
            "priority": {
                "type": "string",
                "enum": [
                    "low",
                    "medium",
                    "high",
                    "critical",
                ],
                "description": (
                    "The priority assigned to the "
                    "escalation."
                ),
            },
        },
        "required": [
            "ticket_id",
            "reason",
            "priority",
        ],
        "additionalProperties": False,
    },
}