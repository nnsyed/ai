Lesson 9 — Streaming + Real-Time Agent UX + Observability
*****************************************************************************************
**I also checked the current OpenAI API documentation before preparing this lesson.**
The current GPT-5.6 family supports the Responses API and function tools; 
gpt-5.6 is currently an alias for GPT-5.6 Sol, 
while gpt-5.6-luna is the lower-cost option.
*****************************************************************************************



So far we have:
                    USER
                      │
                      ▼
                EmployeeAgent
                      │
                      ▼
                OpenAI Responses
                      │
             ┌────────┴────────┐
             │                 │
       Normal answer       Tool call
                               │
                               ▼
                         Tool Registry
                               │
             ┌─────────────────┼────────────────┐
             ▼                 ▼                ▼
         Oracle DB        Calculator        REST API

**Problem defination:**
The problem is that the user doesn't see what is happening.
For example:

You: Calculate BLAKE's compensation and convert it to EUR.
          ... silence ...
AI: BLAKE's annual compensation is €34,xxx.

That's not a great enterprise UX.

Target we want to reach:
You: Calculate BLAKE's compensation and convert it to EUR.

🤖 Understanding request...

🔧 Oracle → get_employee()
✓ Employee found: BLAKE
  Salary: $2,850/month

🔧 Compensation → calculate_compensation()
✓ New salary: $3,049.50/month
✓ Annual compensation: $36,594

🔧 REST → get_exchange_rate()
✓ USD → EUR rate retrieved

🤖 Preparing final answer...

AI:
BLAKE's projected annual compensation is
approximately €31,xxx based on the current
USD/EUR exchange rate.

**3. Three different types of streaming**
This is an important distinction.
1. Text streaming that model generates
B
Bl
Bla
Blak
Blake

2. Tool-call streaming/status
The agent tells us:
Calling get_employee()
Calling calculate_compensation()
Calling get_exchange_rate()

3. Application events
Our application itself generates events:
AGENT_STARTED
TOOL_STARTED
TOOL_COMPLETED
TOOL_FAILED
AGENT_COMPLETED

                         USER
                           │
                           ▼
                     ┌───────────┐
                     │  app.py   │
                     └─────┬─────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ EmployeeAgent   │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Agent State    Event Logger   Metrics
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                   OpenAI Responses
                           │
                    ┌──────┴──────┐
                    │             │
                 Answer        Tool Call
                                  │
                                  ▼
                           Tool Registry
                                  │
                ┌─────────────────┼────────────────┐
                ▼                 ▼                ▼
             Oracle          Calculator         REST

employee-ai-agent/
│
├── app.py
├── config.py
├── requirements.txt
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── events.py
│   └── prompts.py
│
├── tools/
│   ├── oracle_tools.py
│   ├── compensation_tools.py
│   ├── rest_tools.py
│   └── registry.py
│
├── services/
│   ├── oracle_service.py
│   ├── compensation_service.py
│   └── rest_service.py
│
├── tests/
│   ├── test_calculator.py
│   └── test_tools.py
│
└── logs/
    └── agent.log

**Tool execution timing**
One of the most useful observability features is measuring tool execution time.

Example:
get_employee()
   42 ms
calculate_compensation()
    1 ms
get_exchange_rate()
  381 ms

**10. What is perf_counter()?**
We use:
time.perf_counter()

rather than:
time.time()
for measuring durations.

Example:

```
start = time.perf_counter()
do_something()
end = time.perf_counter()
elapsed = end - start
```
Result:
0.381 seconds
This is exactly what we want for performance measurements.

**12. Streaming is slightly more complicated with tools**
This is a very important concept.
With a normal answer:
```
stream = client.responses.create(
    ...,
    stream=True
)
```
we can process:
response.output_text.delta

But with an agent, we may receive:
```
response.created
response.output_item.added
response.function_call_arguments.delta
response.function_call_arguments.done
response.output_item.done
response.completed
```
So an agent streaming loop needs to understand events, rather than simply reading text.
