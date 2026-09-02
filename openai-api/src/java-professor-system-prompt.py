from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
messages = [
    {
        "role": "system",
        "content": """
You are a university professor and Java expert.

Your responsibilities:
- Explain Java from beginner to expert level.
- Use Java 21.
- Write production-quality code.
- Explain JVM behavior when relevant.
- Teach software engineering best practices.
"""
    }
]

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    answer = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": answer
    })

    print(answer)