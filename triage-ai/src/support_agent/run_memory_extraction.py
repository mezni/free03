from support_agent.memory_extraction import (
    extract_memory_candidates,
)


def main():
    message = ""
    """
    My customer ID is C002.

    I prefer to receive support updates by email.
    Please don't call me unless absolutely necessary.
    """

    result = extract_memory_candidates(message)

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()