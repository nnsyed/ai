                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   AI AGENT      │
                  │                 │
                  │      GPT        │
                  └────────┬────────┘
                           │
                 decides which tool
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Department Tool    Employee Tool    Salary Tool
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Oracle    │
                    │   SCOTT     │
                    │             │
                    │ EMP         │
                    │ DEPT        │
                    │ SALGRADE    │
                    └─────────────┘
                           │
                           ▼
                       SQL Result
                           │
                           ▼
                          GPT
                           │
                           ▼
                    Natural Language
                         Answer

The nice thing about this exercise is that the LLM never directly connects to Oracle.

Now our agent has three capabilities:
┌──────────────────────────┐
│      Oracle Agent        │
├──────────────────────────┤
│ get_department()         │
│                          │
│ get_employees_by_dept()  │
│                          │
│ get_salary_statistics()  │
│                          │
└──────────────────────────┘

The instruction we are giving to LLM is to use these three capabilities to answer questions about the database. 
The LLM will decide which capability to use based on the user’s question.

User
 ↓
GPT
 ↓
chooses tool
 ↓
Python
 ↓
Oracle
 ↓
result
 ↓
GPT
 ↓
answer

That sequence is the agent's reasoning/action workflow.

**16. Security — Very Important**
Do not give the LLM arbitrary SQL execution yet.
Example: execute_sql(sql) This is BAD. It is a security risk. 
The LLM could be tricked into executing SQL that drops tables or deletes data.
Instead, give the LLM only the capabilities it needs to answer questions about the database.

19. Lesson 6 Summary
Concept	What we implemented

| Concept             | What we implemented                  |
| ------------------- | ------------------------------------ |
| Real tool           | Python function connected to Oracle  |
| Oracle integration  | `python-oracledb`                    |
| Database tools      | Department, employees, salary        |
| Tool definitions    | JSON schema                          |
| Tool dispatcher     | Maps tool name → Python function     |
| Multi-tool agent    | GPT chooses among tools              |
| Multiple tool calls | Agent can perform sequential actions |
| Agent loop          | LLM → tool → result → LLM            |
| Real data           | SCOTT `EMP`/`DEPT`                   |
| Security boundary   | LLM doesn't directly access Oracle   |
| REST integration    | Architecture ready for it            |
| Enterprise pattern  | DB + REST + LLM                      |

                  ┌───────────────┐
                  │     USER      │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │      GPT      │
                  │               │
                  │ Decide what   │
                  │ to do next    │
                  └───────┬───────┘
                          │
                ┌─────────┼──────────┐
                │         │          │
                ▼         ▼          ▼
             Oracle      REST     Calculator
                │         │          │
                └─────────┼──────────┘
                          │
                          ▼
                     Tool result
                          │
                          ▼
                         GPT
                          │
                          ▼
                    Final answer