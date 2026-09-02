
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

stream = client.responses.create(
    model="gpt-5-mini",
    input="Write a rahat indori's poem",
    stream=True
)

for event in stream:
    print(event)