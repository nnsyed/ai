We will build a small enterprise-style AI agent.
- Oracle SCOTT database
- A real public REST API
- A real compensation calculator
- Bonus calculation
- Salary-increment calculation
- Currency conversion
- Multiple tool calls
- Tool error handling
- Conversation memory
- A reusable project structure

| Tool                          | Purpose                               |
| ----------------------------- | ------------------------------------- |
| `get_department`              | Find department information in Oracle |
| `get_employee`                | Find a specific employee              |
| `get_employees_by_department` | List employees                        |
| `get_salary_statistics`       | Salary analysis                       |
| `calculate_compensation`      | Calculate raise + bonus               |
| `get_exchange_rate`           | Call real public REST API             |
| `get_country_info`            | Optional second REST API              |
| `calculate_currency_amount`   | Convert money                         |

Project Structure:
employee-agent/
│
├── agent.py
│
├── config.py
│
├── oracle_db.py
│
├── calculator.py
│
├── rest_client.py
│
├── tools.py
│
└── requirements.txt

The interesting part is that GPT decides which tools to use.

The Real Compensation Calculator Tool


                 AI Agent
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
    Oracle         REST       Calculator
       │            │            │
       ▼            ▼            ▼
    EMP/DEPT     Employee      Python
                 Service