from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

llm = ChatOpenAI(model="gpt-4.1-mini", 
                 api_key = os.getenv("OPENAI_API_KEY"),
                 temperature=0.7, 
                 max_tokens=500)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert Python instructor."),
        ("human", "Explain {topic} in {lines} lines")
    ])
parser = StrOutputParser()
chain = prompt | llm | parser
answer = chain.invoke({"topic": "lamda functions", "lines": 6})
print(answer)


