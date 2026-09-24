from support_agent.agent import run_agent


def main():
    ticket = """
My internet has been down since this morning.
I restarted my router several times but it still
does not work.
"""

    response = run_agent(ticket)

    print("=" * 60)
    print("AGENT RESPONSE")
    print("=" * 60)
    print(response)


if __name__ == "__main__":
    main()