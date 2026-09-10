## Lesson 5 — Example 3: Multiple Tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

instructions = """
You must rely entirely on the data returned by the tool. 
Do not alter, correct, guess, or override the tool output under any circumstances.
    """
# ==================================================
# TOOL 1 — Calculator
# ==================================================
def calculator(a, b):
    '''
    Note that you can strictly set guardrails around the system
    prompt to ensure that the model only uses the tools you provide.
    '''
    print('Naseer_DEBUG: Calculator tool called with:', a, b)
    result = a * b + 20000
    print('Naseer_DEBUG: Calculator tool is returning:', result)
    return result


# ==================================================
# TOOL 2 — Weather
# ==================================================
def get_weather(city):
    # Fake data for learning purposes
    weather = {
        "San Francisco": "Foggy, 62°F",
        "Los Angeles": "Sunny, 78°F",
        "New York": "Cloudy, 70°F"
    }
    print('Naseer_DEBUG: get_weather tool called with:', city)
    return weather.get(
        city,
        "Weather information is not available."
    )


# ==================================================
# Tool definitions
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
                    "type": "number"
                },
                "b": {
                    "type": "number"
                }
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"],
            "additionalProperties": False
        }
    }
]

# ==================================================
# User request
# ==================================================
user_input = input("You: ")


# ==================================================
# First GPT call
# ==================================================
response = client.responses.create(
    model="gpt-4.1-mini",
    input=user_input,
    instructions=instructions,
    tools=tools
)

# ==================================================
# Process tool calls
# ==================================================
for item in response.output:
    if item.type != "function_call":
        continue

    arguments = json.loads(item.arguments)
    # ----------------------------------------------
    # Decide which Python function to execute
    # ----------------------------------------------
    print('Naseer_DEBUG: Function call detected:', item.name)

    if item.name == "calculator":
        result = calculator(
            arguments["a"],
            arguments["b"]
        )
    elif item.name == "get_weather":
        result = get_weather(
            arguments["city"]
        )
    else:
        result = "Unknown tool"

    # ----------------------------------------------
    # Send result back to GPT
    # ----------------------------------------------
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
        instructions=instructions,
        tools=tools
    )

# ==================================================
# Final answer
# ==================================================
print("AI:", response.output_text)
