from oracle_db import (
    get_department,
    get_employee,
    get_employees_by_department,
    get_salary_statistics
)

from calculator import (
    calculate_compensation,
    convert_currency
)

from rest_client import (
    get_exchange_rate
)

# ==========================================================
# Tool definitions
# ==========================================================
TOOLS = [
    # ------------------------------------------------------
    # Oracle: department
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "get_department",
        "description": """
        Find an Oracle department by name.
        Returns department number, department name
        and location.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "department_name": {
                    "type": "string"
                }
            },
            "required": [
                "department_name"
            ],
            "additionalProperties": False
        }
    },

    # ------------------------------------------------------
    # Oracle: employee
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "get_employee",
        "description": """
        Find an employee in the Oracle EMP table
        using the employee name.
        Returns salary, job, department and other
        employee information.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "employee_name": {
                    "type": "string"
                }
            },
            "required": [
                "employee_name"
            ],
            "additionalProperties": False
        }
    },

    # ------------------------------------------------------
    # Oracle: employees by department
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "get_employees_by_department",
        "description": """
        Get all employees belonging to an Oracle
        department number.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "department_number": {
                    "type": "integer"
                }
            },
            "required": [
                "department_number"
            ],
            "additionalProperties": False
        }
    },
    # ------------------------------------------------------
    # Oracle: salary statistics
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "get_salary_statistics",
        "description": """
        Calculate minimum, maximum and average salary
        for all employees or for a specific department.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "department_number": {
                    "type": [
                        "integer",
                        "null"
                    ]
                }
            },
            "required": [
                "department_number"
            ],
            "additionalProperties": False
        }
    },
    # ------------------------------------------------------
    # Calculator: compensation
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "calculate_compensation",
        "description": """
        Calculate employee compensation.
        The current salary is MONTHLY salary.
        Calculate:
        - salary increase amount
        - new monthly salary
        - percentage bonus
        - fixed bonus
        - annual base salary
        - total annual compensation
        - monthly equivalent compensation
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "current_salary": {
                    "type": "number"
                },
                "raise_percent": {
                    "type": "number"
                },
                "bonus_percent": {
                    "type": "number"
                },
                "fixed_bonus": {
                    "type": "number"
                }
            },
            "required": [
                "current_salary",
                "raise_percent",
                "bonus_percent",
                "fixed_bonus"
            ],
            "additionalProperties": False
        }
    },
    # ------------------------------------------------------
    # REST: exchange rate
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "get_exchange_rate",
        "description": """
        Get the current published exchange rate between
        two currencies using the Frankfurter public
        exchange-rate API.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "base_currency": {
                    "type": "string",
                    "description": "Example: USD"
                },
                "quote_currency": {
                    "type": "string",
                    "description": "Example: EUR"
                }
            },
            "required": [
                "base_currency",
                "quote_currency"
            ],
            "additionalProperties": False
        }
    },
    # ------------------------------------------------------
    # Calculator: currency
    # ------------------------------------------------------
    {
        "type": "function",
        "name": "convert_currency",
        "description": """
        Convert an amount using an exchange rate that
        has already been retrieved.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number"
                },
                "exchange_rate": {
                    "type": "number"
                }
            },
            "required": [
                "amount",
                "exchange_rate"
            ],

            "additionalProperties": False
        }
    }
]

# ==========================================================
# Dispatcher
# ==========================================================
def execute_tool(name,arguments):
    if name == "get_department":
        return get_department(arguments["department_name"])

    if name == "get_employee":
        return get_employee(arguments["employee_name"])

    if name == "get_employees_by_department":
        return get_employees_by_department(arguments["department_number"])

    if name == "get_salary_statistics":
        return get_salary_statistics(arguments["department_number"])

    if name == "calculate_compensation":
        return calculate_compensation(
            arguments["current_salary"],
            arguments["raise_percent"],
            arguments["bonus_percent"],
            arguments["fixed_bonus"]
        )

    if name == "get_exchange_rate":
        return get_exchange_rate(
            arguments["base_currency"],
            arguments["quote_currency"]
        )

    if name == "convert_currency":
        return convert_currency(
            arguments["amount"],
            arguments["exchange_rate"]
        )
    raise ValueError(f"Unknown tool: {name}")

