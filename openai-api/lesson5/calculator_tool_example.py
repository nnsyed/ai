## Lesson 5 — Example 1: A Simple Calculator Tool
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ----------------------------------------
# Our Python tool
# ----------------------------------------
def calculator(a, b):
    return a * b

# ----------------------------------------
# Tell the model about our tool
# ----------------------------------------
tools = [
    {
        "type": "function",
        "name": "calculator",
        "description": "Multiply two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number"
                },
                "b": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    }
]

# ----------------------------------------
# Ask GPT
# ----------------------------------------
response = client.responses.create(
    model="gpt-4.1-mini",
    input="What is 125 multiplied by 37?",
    tools=tools
)

# ----------------------------------------
# Inspect the response
# ----------------------------------------
for item in response.output:
    print("TYPE:", item.type)
    if item.type == "function_call":
        print("Function:", item.name)
        print("Arguments:", item.arguments)
        print("Call ID:", item.call_id)

print(response.output_text)