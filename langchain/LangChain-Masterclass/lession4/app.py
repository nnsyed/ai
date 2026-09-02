import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.runnables import (
    RunnableParallel,
    RunnableBranch
)
load_dotenv()

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)


# --------------------------------------------------
# Sentiment
# --------------------------------------------------
sentiment_prompt = ChatPromptTemplate.from_template(
    """
    Analyze the sentiment of this message.

    Message:
    {message}

    Return only:
    positive, negative, or neutral.
    """
)

sentiment_chain = (
    sentiment_prompt
    | llm
    | StrOutputParser()
)

# --------------------------------------------------
# Category
# --------------------------------------------------
category_prompt = ChatPromptTemplate.from_template(
    """
    Categorize this customer message.

    Message:
    {message}

    Return one category:

    billing
    technical
    shipping
    other
    """
)

category_chain = (
    category_prompt
    | llm
    | StrOutputParser()
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

summary_prompt = ChatPromptTemplate.from_template(
    """
    Summarize this customer complaint in one sentence.

    Message:
    {message}
    """
)

summary_chain = (
    summary_prompt
    | llm
    | StrOutputParser()
)


# --------------------------------------------------
# Run analyses in parallel
# --------------------------------------------------

analysis_chain = RunnableParallel(

    sentiment=sentiment_chain,

    category=category_chain,

    summary=summary_chain
)


# --------------------------------------------------
# Main application
# --------------------------------------------------

message = input(
    "Enter customer message: "
)

result = analysis_chain.invoke(
    {
        "message": message
    }
)


print("\nRESULT")
print("=" * 50)

print(
    "Sentiment:",
    result["sentiment"]
)

print(
    "Category:",
    result["category"]
)

print(
    "Summary:",
    result["summary"]
)