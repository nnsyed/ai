from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

# -----------------------------------------
# Define expected output
# -----------------------------------------
class ReviewAnalysis(BaseModel):
    sentiment: str
    rating: int
    positive_aspects: List[str]
    negative_aspects: List[str]


# -----------------------------------------
# Create OpenAI client
# -----------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# -----------------------------------------
# Customer review
# -----------------------------------------
review = """
The food was excellent but the service was
very slow. The waiter was friendly though.
"""

# -----------------------------------------
# Ask OpenAI for structured output
# -----------------------------------------
response = client.responses.parse(
    model="gpt-5",
    input=f"""
    Analyze this customer review:
    {review}
    """,
    text_format=ReviewAnalysis
)

# -----------------------------------------
# Get parsed result
# -----------------------------------------
result = response.output_parsed

# -----------------------------------------
# Use structured data
# -----------------------------------------
print("Sentiment:", result.sentiment)
print("Rating:", result.rating)
print("Positive:")
for item in result.positive_aspects:
    print("  -", item)

print("Negative:")
for item in result.negative_aspects:
    print("  -", item)