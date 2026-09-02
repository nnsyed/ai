import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Call the Responses API requesting raw JSON
response = client.responses.create(
    model="gpt-5-mini",
    input="List 3 fictional fruits, their colors, and taste descriptions. Return the output as a valid JSON object.",
    text={
        "format": {
            "type": "json_object"
        }
    }
)

# 1. Grab the raw JSON string from the response
raw_json_string = response.output_text

# 2. Parse the string into a native Python dictionary
data = json.loads(raw_json_string)

# 3. Print the result nicely formatted
print(json.dumps(data, indent=4))