# Lesson 2 — Chatbot With Conversation Memory
from openai import OpenAI
from dotenv import load_dotenv
import os


def main():

    # ------------------------------------------------
    # 1. Create OpenAI client
    # ------------------------------------------------
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # ------------------------------------------------
    # 2. Create conversation history
    # ------------------------------------------------
    conversation = []

    print("=" * 60)
    print("             AI Chatbot - Lesson 2")
    print("=" * 60)
    print("Conversation memory enabled.")
    print("Type 'exit' to quit.")
    print()

    # ------------------------------------------------
    # 3. Chat loop
    # ------------------------------------------------
    while True:

        user_input = input("You: ")

        # ------------------------------------------------
        # Exit
        # ------------------------------------------------
        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break

        # ------------------------------------------------
        # Add user's message to conversation
        # ------------------------------------------------
        conversation.append({
            "role": "user",
            "content": user_input
        })

        # ------------------------------------------------
        # Send complete conversation to OpenAI
        # ------------------------------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=conversation
        )

        # ------------------------------------------------
        # Extract AI response
        # ------------------------------------------------
        answer = response.output_text

        print()
        print("AI:", answer)
        print()

        # ------------------------------------------------
        # Add AI response to conversation
        # ------------------------------------------------
        conversation.append({
            "role": "assistant",
            "content": answer
        })

        # ------------------------------------------------
        # Display token usage
        # ------------------------------------------------
        if response.usage:

            print("Token Usage")
            print("------------")
            print(
                "Input tokens :",
                response.usage.input_tokens
            )
            print(
                "Output tokens:",
                response.usage.output_tokens
            )
            print(
                "Total tokens :",
                response.usage.total_tokens
            )

        print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
