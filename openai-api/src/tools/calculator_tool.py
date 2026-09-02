import json

def calculate(operation: str, num1: float, num2: float) -> str:
    """Perform basic math calculations."""
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else "Error: Division by zero"
    }
    
    result = operations.get(operation.lower(), "Error: Invalid operation")
    return json.dumps({"result": result})

# Agent Tool Definition
calculate_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Performs basic arithmetic operations like addition, subtraction, multiplication, and division.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The math operation to perform."
                },
                "num1": {"type": "number", "description": "The first number."},
                "num2": {"type": "number", "description": "The second number."}
            },
            "required": ["operation", "num1", "num2"]
        }
    }
}

calculate("add", 5, 3)  # Example usage)