from openai import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    # Create the OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # -----------------------------------------
    # Conversation memory
    # -----------------------------------------
    conversation = []

    # -----------------------------------------
    # Instructions for the AI
    # -----------------------------------------
    instructions = """
    You are an expert Python tutor.

    Explain concepts in simple language.

    Always provide a small example when useful.

    Break complicated concepts into smaller steps.

    If the user asks for code, explain the code
    after providing it.
    """

    print("=" * 60)
    print("              Python AI Tutor")
    print("=" * 60)
    print("Type 'exit' to quit.")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break

        # -----------------------------------------
        # Add user message
        # -----------------------------------------
        conversation.append({
            "role": "user",
            "content": user_input
        })

        # -----------------------------------------
        # Call OpenAI
        # -----------------------------------------
        response = client.responses.create(
            model="gpt-5",
            instructions=instructions,
            input=conversation
        )

        # -----------------------------------------
        # Get answer
        # -----------------------------------------
        answer = response.output_text

        print()
        print("AI:", answer)
        print()

        # -----------------------------------------
        # Store AI response
        # -----------------------------------------
        conversation.append({
            "role": "assistant",
            "content": answer
        })

        # -----------------------------------------
        # Token usage
        # -----------------------------------------
        if response.usage:

            print(
                f"Tokens: "
                f"{response.usage.input_tokens} input, "
                f"{response.usage.output_tokens} output, "
                f"{response.usage.total_tokens} total"
            )

        print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
