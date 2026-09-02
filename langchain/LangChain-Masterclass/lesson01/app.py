from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# ----------------------------------------------------
# Load the environment variables from .env
# ----------------------------------------------------
load_dotenv()

# ----------------------------------------------------
# Read the OpenAI API key
# ----------------------------------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Please check your .env file."
    )

# ----------------------------------------------------
# Create the chat model
# ----------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=api_key,
    temperature=0.7,
)

# ----------------------------------------------------
# Ask a question
# ----------------------------------------------------
reprompt = "Can you please generate a short overview of the Third Battle of Panipat?"
response = llm.invoke(reprompt)
print(response.content)

