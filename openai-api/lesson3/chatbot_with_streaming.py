from openai import OpenAI
from dotenv import load_dotenv
import os

def main():

    # -----------------------------------------
    # Create OpenAI client
    # -----------------------------------------
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # -----------------------------------------
    # Conversation history
    # -----------------------------------------
    conversation = []

    # -----------------------------------------
    # AI instructions
    # -----------------------------------------
    instructions = """
    You are an expert Python programming tutor.
    Explain concepts clearly and simply.
    Give examples when appropriate.
    When providing code, explain the important
    parts of the code.
    """

    print("=" * 60)
    print("          Python AI Tutor - Lesson 3")
    print("=" * 60)
    print("Streaming responses enabled.")
    print("Type 'exit' to quit.")
    print()

    # -----------------------------------------
    # Chat loop
    # -----------------------------------------
    while True:
        user_input = input("You: ")
        # -----------------------------------------
        # Exit
        # -----------------------------------------
        if user_input.lower() == "exit":

            print("AI: Goodbye!")
            break

        # -----------------------------------------
        # Clear conversation
        # -----------------------------------------
        if user_input.lower() == "clear":
            conversation = []
            print("AI: Conversation cleared.")
            print()
            continue

        # -----------------------------------------
        # Add user message
        # -----------------------------------------
        conversation.append({
            "role": "user",
            "content": user_input
        })

        print()
        print("AI: ", end="", flush=True)

        # -----------------------------------------
        # Create streaming response
        # -----------------------------------------
        stream = client.responses.create(
            model="gpt-5",
            instructions=instructions,
            input=conversation,
            stream=True
        )

        # -----------------------------------------
        # Collect complete AI response
        # -----------------------------------------
        answer = ""

        # -----------------------------------------
        # Process streaming events
        # -----------------------------------------
        for event in stream:
            if event.type == "response.output_text.delta":
                text = event.delta
                # Display immediately
                print(text, end="", flush=True)
                # Save for conversation history
                answer += text
        print()
        print()

        # -----------------------------------------
        # Add complete AI response to history
        # -----------------------------------------
        conversation.append(
            {
            "role": "assistant",
            "content": answer
            })

        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
