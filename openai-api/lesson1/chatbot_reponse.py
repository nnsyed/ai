from openai import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    # -----------------------------------------
    # 1. Create OpenAI client
    # -----------------------------------------
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    print("=" * 60)
    print("              My First AI Chatbot")
    print("=" * 60)
    print("Type 'exit' to quit.")
    print()

    # -----------------------------------------
    # 2. Chat loop
    # -----------------------------------------
    while True:
        user_input = input("You: ")

        # -----------------------------------------
        # 3. Exit
        # -----------------------------------------
        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break

        # -----------------------------------------
        # 4. Call OpenAI
        # -----------------------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_input
        )

        # -----------------------------------------
        # 5. Extract answer
        # -----------------------------------------
        answer = response.output_text

        print()
        print("AI:", answer)

        # -----------------------------------------
        # 6. Display token usage
        # -----------------------------------------
        if response.usage:

            print()
            print("Token Usage")
            print("-----------")
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
