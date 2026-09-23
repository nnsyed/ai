So far we have done this

                    USER
                    │
                    ▼
             ┌─────────────┐
             │     GPT     │
             └──────┬──────┘
                    │
           chooses a tool
                    │
       ┌────────────┼─────────────┐
       ▼            ▼             ▼
    Oracle       Calculator      REST
       │            │             │
       └────────────┼─────────────┘
                    ▼
                   GPT
                    │
                    ▼
              FINAL ANSWER

But imagine you now have:
25 tools
10 REST services
3 databases
authentication
logging
auditing
retry policies
business rules
multiple developers
unit tests

Putting everything into agent.py quickly becomes a mess.

So refactor:

employee-ai-agent/
│
├── app.py
│
├── config.py
│
├── requirements.txt
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── prompts.py
│   └── memory.py
│
├── tools/
│   ├── __init__.py
│   ├── oracle_tools.py
│   ├── compensation_tools.py
│   ├── rest_tools.py
│   └── registry.py
│
├── services/
│   ├── __init__.py
│   ├── oracle_service.py
│   └── rest_service.py
│
├── tests/
│   ├── test_calculator.py
│   └── test_tools.py
│
└── logs/


┌──────────────────────────────────────────┐
│                  app.py                  │
│             User Interface               │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│               agent.py                   │
│             Agent Runtime                │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│              Tool Registry               │
└───────────────┬──────────┬───────────────┘
                │          │
                ▼          ▼
          Oracle Tools   REST Tools
                │          │
                ▼          ▼
           Oracle DB    REST APIs

                     +
                     
              Compensation
                 Tools


**Why do we have a Service Layer?**
This is a common enterprise design pattern.

We don't want this:
GPT
 ↓
Tool
 ↓
SQL
 ↓
Oracle

Instead:
GPT
 ↓
Tool
 ↓
Service
 ↓
Oracle

Example:
get_employee()
       │
       ▼
OracleService
       │
       ▼
Oracle DB

Why? Because tomorrow we might want:



| Area           | Lesson 8                        |
| -------------- | ------------------------------- |
| Architecture   | Layered application             |
| UI             | `app.py`                        |
| Agent          | `EmployeeAgent`                 |
| Prompt         | Separate system instructions    |
| Memory         | Dedicated component             |
| Tools          | Dedicated modules               |
| Tool registry  | Centralized                     |
| Services       | Oracle / REST / business logic  |
| Oracle         | Isolated service                |
| REST           | Isolated service                |
| Calculator     | Deterministic business service  |
| Security       | Tool allowlist                  |
| Error handling | Tool failures returned to agent |
| Logging        | Python logging                  |
| Testing        | Pytest                          |
| Configuration  | Environment variables           |


Whis is this architecture better?
old design:
agent.py
    │
    ├── Oracle
    ├── SQL
    ├── REST
    ├── calculator
    ├── tools
    ├── prompts
    ├── memory
    └── UI


new design:
                app.py
                   │
                   ▼
                Agent
                   │
                   ▼
             Tool Registry
          ┌────────┼────────┐
          ▼        ▼        ▼
       Oracle   Calculator  REST
          │        │        │
          ▼        ▼        ▼
       Service   Service   Service
This is much easier to:
- maintain
- test
- extend
- secure
- deploy
- debug

**A Major Concept: Tools vs Services**
This distinction is worth remembering.

**Service**: is a software component that exists independently of AI. It can be used by 
any client, human or machine. It has its own API, business logic, and data access.
- OracleService
- RestService
- CompensationService

**Tool**: is an LLM-facing interface that makes a service available to the AI. It is a thin wrapper around a service,
- get_employee
- get_exchange_rate
- calculate_compensation

So:

               LLM
                │
                ▼
              TOOL
                │
                ▼
             SERVICE
                │
                ▼
          Database/API

- The service exists independently of AI.
- The tool exists specifically to make a capability available to the AI.
- That's an excellent enterprise design pattern.

**Tool Schema vs Python Function**
We actually have two representations of every tool.
1. In python , a tool is a function that takes arguments and returns a result.
It tells Python how to execute it.

'''
def get_employee(employee_name):
'''

2. LLM Schema: a tool is a JSON schema that describes the function's arguments and return value. 
The LLM uses this schema to generate valid calls to the tool.
It tells GPT how to use it.
{
    "type": "function",
    "name": "get_employee",
    "description": "Find an employee...",
    "parameters": {
        "type": "object",
        "properties": {
            "employee_name": {
                "type": "string"
            }
        }
    }
}

That loop is the heart of our agent.
                         ┌──────────────┐
                         │     USER     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   app.py     │
                         └──────┬───────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   EmployeeAgent    │
                     │                    │
                     │ GPT + Agent Loop   │
                     └─────────┬──────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │ Tool Registry   │
                      └───────┬─────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Oracle Tools    Compensation      REST Tools
             │             Tools              │
             ▼                ▼                ▼
        OracleService   CompensationService  RestService
             │                │                │
             ▼                ▼                ▼
          Oracle DB       Python logic    Public REST API



| -------------- | ------------------------------- |
| Area           | Lesson 8                        |
| -------------- | ------------------------------- |
| Architecture   | Layered application             |
| UI             | `app.py`                        |
| Agent          | `EmployeeAgent`                 |
| Prompt         | Separate system instructions    |
| Memory         | Dedicated component             |
| Tools          | Dedicated modules               |
| Tool registry  | Centralized                     |
| Services       | Oracle / REST / business logic  |
| Oracle         | Isolated service                |
| REST           | Isolated service                |
| Calculator     | Deterministic business service  |
| Security       | Tool allowlist                  |
| Error handling | Tool failures returned to agent |
| Logging        | Python logging                  |
| Testing        | Pytest                          |
| Configuration  | Environment variables           |
