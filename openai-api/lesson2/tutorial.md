**Lesson 2 — Building a Chatbot With Conversation Memory**

**Important Concept — The Model Doesn't Have Memory**
The model receives the request. It **does not mean** that your Python application automatically maintains unlimited conversation memory.
Your application needs to manage the conversation state appropriately.

User
 │
 │ "What is recursion?"
 ▼
Python
 │
 │ API request
 ▼
OpenAI
 │
 ▼
Answer
 │
 ▼
Terminal


Then, when the user asked another question:
User
 │
 │ "Give me an example"
 ▼
Python
 │
 ▼
OpenAI

The second request didn't automatically contain the previous conversation. So the model may not know what "it" or "that" refers to.

Think of it as:

                 Your Application
                       │
             ┌─────────┴─────────┐
             │ Conversation State│
             └─────────┬─────────┘
                       │
                       ▼
                  OpenAI Model


The basic idea is to maintain a conversation state in your application (in a python list).


Your application is responsible for maintaining the context you want the model to use.
**First Memory Implementation**
```
conversation = []
conversation.append({
    "role": "user",
    "content": user_input
})
conversation.append({
    "role": "assistant",
    "content": answer
})
```

**Why role Matters?**
These identify who produced the message.
Example:
USER
  │
  └── What is Python?

ASSISTANT
  │
  └── Python is a programming language.

USER
  │
  └── What can I build with it?


**System Level Instructions** are instructions that are provided to the model to guide its behavior. 
They can be used to set the tone, style, or specific guidelines for how the model should respond.



**Problem with Conversation Memory** 
Our conversation keeps growing:
Message 1
Message 2
Message 3
Message 4
Message 5
...
Message 100
Message 101
Message 102

Eventually, we need strategies for:
- limiting history
- summarizing old conversations
- storing conversations externally
- retrieving only relevant history
- managing context windows

These become important Agent architecture concepts.

You can clear the conversation list as a workaround:
```
if user_input.lower() == "clear":

    conversation = []

    print("AI: Conversation cleared.")
    continue
```



Inital archirecture:

          User
           │
           ▼
        Python
           │
           ▼
          LLM
           │
           ▼
         Answer

Now:

                 ┌──────────────────┐
                 │ Conversation     │
                 │     History      │
                 └────────┬─────────┘
                          │
                          ▼
User ────────► Python Application
                          │
                          ▼
                       OpenAI
                          │
                          ▼
                        Answer
                          │
                          ▼
                 Conversation History


**What we have learned so far:**
┌────────────────────────────────────────────────────────┐
| Concept              | Lesson 2                        |
| -------------------- | ------------------------------- |
| Conversation history | Store previous messages         |
| `conversation`       | Application state               |
| `role=user`          | User message                    |
| `role=assistant`     | Model response                  |
| `instructions`       | Define model behavior           |
| Context              | Give model previous information |
| `clear`              | Reset application state         |
| Token growth         | More history means more input   |
└────────────────────────────────────────────────────────┘


**important take away:**
             AI MODEL
                ▲
                │
       conversation context
                │
                │
User ─────► Your Application
                │
                │
         manages the state