import json

from tools.oracle_tools import (
    get_employee,
    get_department,
    get_employees_by_department,
    get_salary_statistics
)

from tools.compensation_tools import (
    calculate_compensation
)

from tools.rest_tools import (
    get_exchange_rate
)

# ==========================================================
# Python function registry
# ==========================================================
FUNCTIONS = {
    "get_employee": get_employee,
    "get_department": get_department,
    "get_employees_by_department": get_employees_by_department,
    "get_salary_statistics": get_salary_statistics,
    "calculate_compensation": calculate_compensation,
    "get_exchange_rate": get_exchange_rate
}

# ==========================================================
# OpenAI tool definitions
# ==========================================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "get_employee",
        "description": """
        Find an employee in the Oracle EMP table.
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
    {
        "type": "function",
        "name": "get_department",
        "description": """
        Find an Oracle department by name.
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
    {
        "type": "function",
        "name":
            "get_employees_by_department",
        "description": """
        Get employees belonging to a department.
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
    {
        "type": "function",
        "name":
            "get_salary_statistics",
        "description": """
        Calculate salary statistics for all employees
        or a specific department.
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
    {
        "type": "function",
        "name":
            "calculate_compensation",
        "description": """
        Calculate compensation using a monthly salary.
        Calculates:
        - raise amount
        - new monthly salary
        - percentage bonus
        - fixed bonus
        - annual base salary
        - total annual compensation
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
    {
        "type": "function",
        "name":
            "get_exchange_rate",
        "description": """
        Get a current exchange rate between two currencies
        using the Frankfurter public API.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "base_currency": {
                    "type": "string"
                },
                "quote_currency": {
                    "type": "string"
                }
            },
            "required": [
                "base_currency",
                "quote_currency"
            ],
            "additionalProperties": False
        }
    }
]

# ==========================================================
# Dispatcher
# ==========================================================
def execute_tool(tool_name, arguments):
    function = FUNCTIONS.get(tool_name)

    if function is None:
        raise ValueError(f"Tool not authorized: "  f"{tool_name}")

    return function(**arguments)
