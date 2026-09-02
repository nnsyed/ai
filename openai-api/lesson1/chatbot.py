from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Create the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Display application title
print("=" * 50)
print("           My First AI Chatbot")
print("=" * 50)
print("Type 'exit' to quit.")
print()

while True:
    # Get input from the user
    user_input = input("You: ")

    # Check whether the user wants to exit
    if user_input.lower() == "exit":
        print("AI: Goodbye!")
        break

    # Send the user's question to OpenAI
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_input
    )

    # Extract the generated text
    answer = response.output_text

    # Display the answer
    print("AI:", answer)
    print()
