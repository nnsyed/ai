from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Flattened definition schema for client.responses.create
weather_tool = {
    "type": "function",
    "name": "get_current_weather",
    "description": "Get the current weather for a specific location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}
        },
        "required": ["location"]
    }
}

response = client.responses.create(
    model="gpt-4.1-mini",
    input="What is the weather like in Paris right now?",
    tools=[weather_tool]
)

for item in response.output:
    if item.type == "function_call":
        print(f"Requested Tool: {item.name}")
        
        # Parse the JSON arguments string
        args = json.loads(item.arguments)
        print(f"Arguments: {args}")
        print(f"Location extracted: {args.get('location')}")
        print(f"Call ID to submit back: {item.call_id}")