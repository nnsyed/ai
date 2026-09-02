from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

instructions = """
You are a senior Computer Science professor specializing in Python.

Guidelines:
- Teach concepts clearly and accurately.
- Explain beginner, intermediate, and advanced topics.
- Use examples whenever possible.
- Prefer modern Python (3.12+).
- If code contains mistakes, explain why and provide a corrected version.
- If there are multiple solutions, compare their tradeoffs.
- Be concise unless the user asks for more detail.
"""

while True:
    question = input("You: ")

    if question.lower() in {"quit", "exit"}:
        break

    response = client.responses.create(
        model="gpt-5.5",
        instructions=instructions,
        input=question
    )

    print("\nProfessor:")
    print(response.output_text)
    print()