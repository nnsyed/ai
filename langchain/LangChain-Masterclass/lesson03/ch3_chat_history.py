'''
Problem:

  Question 1
     │
     ▼
  Answer

  Question 2
     │
     ▼
  Answer

  The model has no memory of previous interactions.

  You : My name is Naseer.

  AI : Nice to meet you!

  You : What is my name?

the model won't know the answer unless we send the earlier conversation again.

Lesson 3 — Conversations, Messages, Chat History & Memory
---------------------------------------------------------
Request #1
User: My name is Naseer.

When the API sends the second request, it will also send the previous information.
Request #2
System: You are helpful.
Human: My name is Naseer.
AI: Nice to meet you, Naseer!
Human: What is my name?

This is a fundamental concept that every AI engineer should understand.

'''


'''
A conversation is simply a list of messages.
[
SystemMessage(...),
HumanMessage(...),
AIMessage(...),
HumanMessage(...),
AIMessage(...)
]
'''

from langchain_core.messages import (HumanMessage, AIMessage, SystemMessage)
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My name is Naseer."),
    AIMessage(content="Nice to meet you!"),
    HumanMessage(content="What is my name?")
]
for message in messages:
    print(type(message).__name__)
    print(message.content)
    print("-" * 40)

'''
The Problem: Imagine a conversation with 300 messages.
Would you manually create?
messages.append(...)
after every response?

Of course not!!!

We need something smarter.

Introducing Chat History

LangChain provides a message history object.
from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)
'''

from langchain_core.chat_history import (InMemoryChatMessageHistory)
history = InMemoryChatMessageHistory()

history.add_user_message("My name is Naseer.")
history.add_ai_message("Nice to meet you!")
history.add_user_message("What is my name?")
history.add_user_message("I live in California.")
history.add_ai_message("Great!")
print(history.messages)

'''
Message Place Holders
=====================
This is where prompt templates become powerful.


But where do previous messages go?
Between the system prompt and the latest question.
LangChain provides a placeholder.


When you run this prompt, take whatever messages are stored in history and put them right here

System Prompt
      ↓
   {history}
      ↓
Latest Question


5. Why is it called a "placeholder"?

Think about a Word document template.

You might have:
Dear ______,
Welcome to our company.
The blank ______ is a placeholder. Later, you insert a name there.
MessagesPlaceholder works similarly.

You have:
MessagesPlaceholder(variable_name="history")
which is essentially saying:
Put the contents of "history" here.



Your application
      │
      │ stores conversation
      ↓
history = [
   Human message,
   AI message,
   Human message,
   AI message
]
      │
      ↓
MessagesPlaceholder("history")
      │
      ↓
Prompt
      │
      ↓
Chat Model

'''

from langchain_core.prompts import (MessagesPlaceholder)
prompt = ChatPromptTemplate.from_messages(
[
    ("system","You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human","{question}")
])

'''
RunnableWithMessageHistory
Now comes the really clever part.
Instead of manually managing messages, LangChain can do it automatically.


from langchain_core.runnables.history import (RunnableWithMessageHistory)
chain = prompt | llm | parser
chain_with_history = RunnableWithMessageHistory(chain, get_history, input_messages_key="question", history_messages_key="history")

'''

'''
What is get_history()?
Imagine multiple users.
Alice
Bob
Charlie

Each person needs their own conversation.
Not one giant shared history.
We create a dictionary.
store = {}
Then

def get_history(session_id):
    if session_id not in store:
        store[session_id] = ( InMemoryChatMessageHistory() )
    return store[session_id]

Now every session gets its own history.

session_1
↓
Conversation A
-------------------
session_2
↓
Conversation B
'''