from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

class Person(BaseModel):
    name: str
    age: int
    job: str
    company: str
    location: str

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

text = """
John Smith is a 42 year old software engineer
working at Oracle. He lives in California.
"""


response = client.responses.parse(
    model="gpt-5",
    input=f"""
    Extract the person's information.
    Text:
    {text}
    """,
    text_format=Person
)

person = response.output_parsed
print("Name:", person.name)
print("Age:", person.age)
print("Job:", person.job)
print("Company:", person.company)
print("Location:", person.location)
