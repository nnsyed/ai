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
    # 2. Conversation api
    # ------------------------------------------------
    conversation = client.conversations.create()

    # ------------------------------------------------
    # 3. Call OpenAI and get the response id
    # ------------------------------------------------    
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="my name is naseer and I am 22 years old.",
        conversation=conversation.id
    )

    print("Response ID:" + response.id)
    print("response text:" + response.output_text)

    # -----------------------------------------
    # 4. Call OpenAI again and print the response using the response id
    # -----------------------------------------
    responseReg = client.responses.create(
        model="gpt-4.1-mini",
        input="what is my name?",
        conversation=conversation.id
    )

    answer = responseReg.output_text
    print()
    print("AI:", answer)

if __name__ == "__main__":
    main()
