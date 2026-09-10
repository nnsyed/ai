## Lesson 5 — Example 2: Complete Calculator Agent
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ==================================================
# 1. Define our Python function
# ==================================================
def calculator(a, b):
    return a * b

# ==================================================
# 2. Describe the function to GPT
# ==================================================
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

# ==================================================
# 3. User request
# ==================================================
user_input = "What is 125 multiplied by 37?"

# ==================================================
# 4. First call to GPT
# ==================================================
response = client.responses.create(
    model="gpt-4.1-mini",
    input=user_input,
    tools=tools
)

# ==================================================
# 5. Examine GPT's output
# ==================================================
for item in response.output:
    if item.type == "function_call":
        print("GPT requested a tool call")
        print("Function:", item.name)
        print("Arguments:", item.arguments)

        # ------------------------------------------
        # Convert JSON arguments into Python object
        # ------------------------------------------
        arguments = json.loads(item.arguments)

        # ------------------------------------------
        # Execute our Python function
        # ------------------------------------------
        result = calculator(
            arguments["a"],
            arguments["b"]
        )
        print("Tool result:", result)

        # ------------------------------------------
        # Send tool result back to GPT
        # ------------------------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(result)
                }
            ],
            tools=tools
        )

# ==================================================
# 6. Print final answer
# ==================================================
print("\nAI:", response.output_text)
