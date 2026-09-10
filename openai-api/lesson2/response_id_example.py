# Lesson 2 — Chatbot With Conversation Memory: We are passing the response from previous
# user messages to the model so it can remember the conversation.

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
    # 2. Call OpenAI and get the response id
    # ------------------------------------------------
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="my name is naseer and I am 22 years old."
    )

    print("Response ID:" + response.id)
    print("response text:" + response.output_text)

    # -----------------------------------------
    # 3. Call OpenAI again and print the response using the response id
    # -----------------------------------------
    responseReg = client.responses.create(
        model="gpt-4.1-mini",
        input="what is my name?",
        previous_response_id=response.id
    )

    answer = responseReg.output_text
    print()
    print("AI:", answer)

if __name__ == "__main__":
    main()
