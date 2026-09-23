import logging
from agent.agent import EmployeeAgent

# ==========================================================
# Logging
# ==========================================================
logging.basicConfig(level=logging.INFO,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "%(message)s"
    )
    handlers=[logging.FileHandler( "logs/agent.log" ),logging.StreamHandler()]
)


# ==========================================================
# Application
# ==========================================================

def main():
    agent = EmployeeAgent()
    print()
    print("==============================================")
    print("       Oracle Employee AI Assistant")
    print("==============================================")
    print()
    print("Commands:")
    print("  exit  - quit")
    print("  reset - start a new conversation")
    print()

    while True:
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            break

        if question.lower() == "reset":
            agent = EmployeeAgent()

            print("Conversation reset.")
            continue
        try:
            answer = agent.ask(question)
            print()
            print("AI:", answer)
            print()

        except Exception as exc:
            print()
            print("Application error:",exc)
            print()

if __name__ == "__main__":
    main()