**Lesson 5 — Tool / Function Calling**
-------------------------------------------
We will add multiple tools to our LLM application. 
The tools will be functions that the LLM can call to perform specific tasks. 
This allows us to extend the capabilities of the LLM beyond just generating text.

                 AI Agent
                    │
          ┌─────────┼──────────┐
          │         │          │
          ▼         ▼          ▼
      Calculator  Weather   Database
        Tool       Tool       Tool

The really important part will be that the model itself chooses which tool to call 
based on the user's request. That is the point where our simple chatbot starts becoming 
a genuine AI Agent.

**What is a tool?**
A tool is simply a capability that your application exposes to the model.
For example:
- calculator
- get_weather
- search_database
- send_email
- create_ticket
- get_stock_price
- execute_sql

The important distinction is:

**The LLM does not actually execute your Python function.**

The LLM says:
"I want to call calculator with these arguments."
**Your Python application receives that request, executes the function, and sends the result back.**


**The three pieces of a tool**
When we define a tool, we're really giving GPT three things.

**1. Name**
"name": "calculator"
**2. Description**
"description": "Multiply two numbers together."

**3. Parameters**
"parameters": {
    "type": "object",
    "properties": {
        "a": {"type": "number"},
        "b": {"type": "number"}
    },
    "required": ["a", "b"]
}

**The model uses this information to decide: "Can this tool help answer the user's question?"**

We need to:
- Send request to GPT.
- Detect a function call.
- Extract the arguments.
- Call our Python function.
- Send the result back to GPT.
- Get the final answer.

In calculator_tool_fullexample.py, 

            CALL #1
User ──────────────────────► GPT
                             │
                             │ function_call
                             ▼
                         Python code
                             │
                             │ calculator()
                             ▼
                           4625
                             │
             CALL #2        │
GPT ◄────────────────────────┘
 │
 ▼
Final answer


**Why call_id is important?**
When we call GPT for the first time, we get a response with a call_id. 
When we send the result of our function back to GPT, we need to include 
that call_id.

This becomes particularly important when an agent makes **multiple tool calls.**

                         ┌──────────────┐
                         │     GPT      │
                         │              │
                         │ Tool Router  │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        Calculator          Weather           Database
              │                 │                 │
              ▼                 ▼                 ▼
           Python            API call          Oracle DB

The model is acting as a router

**This is the beginning of an AI Agent.**


**IMPORTANT NOTE:Tool calling vs Structured Output**

To a model you ask: **Analyze this text** and give me a JSON object with the following fields: name, age, and city.
The model will respond with a JSON object. **This is structured output.**

Example:
Ask GPT: -> Analyze this support ticket.

You receive: 
{
    "category": "database",
    "priority": "high",
    "requires_human": true
}
**The model is producing data.**

In Tool Calling, the model is producing a function call. It is saying: "I want to call this function with these arguments."
Example:
You ask GPT: -> What is 125*37

You receive:
{
    "name": "calculator",
    "arguments": {
        "a": 125,
        "b": 37
    }
}

**The model is requesting an action.**

Structured Output
       ↓
     DATA


Tool Calling
       ↓
     ACTION

**This distinction will become extremely useful when we get to LangChain and LangGraph.**


**Tool calling is NOT autonomous execution**
Your application decides whether to execute it.

             GPT
              │
       "Please delete DB"
              │
              ▼
       Your application
              │
       ┌──────┴──────┐
       │             │
     allow         reject
       │             │
       ▼             ▼
    execute       cancel



   **Archirectural overview**
┌──────────────────────────────────────────┐
│                AI AGENT                  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │               GPT                  │  │
│  │                                    │  │
│  │ Understand → Reason → Choose Tool  │  │
│  └──────────────────┬─────────────────┘  │
│                     │                    │
│                     ▼                    │
│              Tool Selection              │
│                     │                    │
│       ┌─────────────┼─────────────┐      │
│       ▼             ▼             ▼      │
│  Calculator      Weather       Database  │
│       │             │             │      │
│       └─────────────┼─────────────┘      │
│                     ▼                    │
│                 Tool Result              │
│                     │                    │
│                     ▼                    │
│                    GPT                   │
│                     │                    │
│                     ▼                    │
│               Final Response             │
└──────────────────────────────────────────┘