**Lesson 2 — Building a Chatbot With Conversation Memory**

**Important Concept — The Model Doesn't Have Memory**
The model receives the request. It does not mean that your Python application automatically maintains unlimited conversation memory.
Your application needs to manage the conversation state appropriately.

Think of it as:

                 Your Application
                       │
             ┌─────────┴─────────┐
             │ Conversation State│
             └─────────┬─────────┘
                       │
                       ▼
                  OpenAI Model

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