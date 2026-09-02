from dotenv import load_dotenv 
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.responses.create(
    model="gpt-4.1-mini",
    input="""
    Extract the product information and return the result as JSON.

    Laptop Dell XPS
    Price 1200 dollars
    Rating 4.8
    """,
    text={
        "format": {
            "type": "json_object"
        }
    }
)

print(response.output_text)