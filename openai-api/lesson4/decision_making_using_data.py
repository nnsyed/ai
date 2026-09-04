from openai import OpenAI
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import os

class SupportTicket(BaseModel):
    category: Literal[
        "database",
        "network",
        "security",
        "application",
        "other"
    ]
    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]
    summary: str
    requires_human: bool

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
ticket = """
Our production database server is down.
All applications are failing.
Customers cannot access the system.
"""

response = client.responses.parse(
    model="gpt-5",
    input=f"""
    Analyze this support ticket:
    {ticket}
    """,
    text_format=SupportTicket
)

result = response.output_parsed
print("Category:", result.category)
print("Priority:", result.priority)
print("Summary:", result.summary)
print("Human required:", result.requires_human)
