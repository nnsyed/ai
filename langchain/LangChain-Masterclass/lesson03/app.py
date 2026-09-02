from dotenv import load_dotenv
import os

from dotenv.main import _load_dotenv_disabled
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_history(session_id):
    if session_id not in store:
        store[session_id] = (InMemoryChatMessageHistory())
    return store[session_id]


load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a friendly assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

parser = StrOutputParser()

chain = prompt | llm | parser
store = {}

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history=get_history,
    input_messages_key="question",
    history_messages_key="history")

session_id = "lesson3-demo"

while True:
    question = input("\nYou: ")
    if question.lower() == "quit":
        break

    answer = conversation.invoke(
        {"question": question},
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    print("\nAI:", answer)

history = get_history("lesson3-demo")
for msg in history.messages:
    print(type(msg).__name__)
    print(msg.content)
    print("-" * 50)
