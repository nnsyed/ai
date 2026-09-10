import os
import json
import oracledb
from dotenv import load_dotenv
from openai import OpenAI

# ============================================================
# OPENAI
# ============================================================
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ============================================================
# ORACLE CONNECTION
# ============================================================
def get_connection():
    return oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    )


# ============================================================
# TOOL 1
# ============================================================
def get_department(department_name):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT DEPTNO, DNAME, LOC
            FROM DEPT
            WHERE UPPER(DNAME) = UPPER(:name)
        """
        cursor.execute(
            sql,
            name=department_name
        )
        row = cursor.fetchone()
        if row is None:
            return 
            {
                "found": False,
                "message": "Department not found"
            }
        return 
        {
            "found": True,
            "department_number": row[0],
            "department_name": row[1],
            "location": row[2]
        }
    finally:
        connection.close()

# ============================================================
# TOOL 2
# ============================================================
def get_employees_by_department(department_number):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
            SELECT
                EMPNO,
                ENAME,
                JOB,
                SAL,
                COMM
            FROM EMP
            WHERE DEPTNO = :deptno
            ORDER BY SAL DESC
        """
        cursor.execute(
            sql,
            deptno=department_number
        )
        employees = []
        for row in cursor:
            employees.append({
                "employee_number": row[0],
                "name": row[1],
                "job": row[2],
                "salary":
                    float(row[3])
                    if row[3] else None,
                "commission":
                    float(row[4])
                    if row[4] else None
            })

        return employees
    finally:
        connection.close()

# ============================================================
# TOOL 3
# ============================================================
def get_salary_statistics(department_number=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        if department_number is None:

            sql = """
                SELECT
                    COUNT(*),
                    MIN(SAL),
                    MAX(SAL),
                    AVG(SAL)
                FROM EMP
            """
            cursor.execute(sql)
        else:
            sql = """
                SELECT
                    COUNT(*),
                    MIN(SAL),
                    MAX(SAL),
                    AVG(SAL)
                FROM EMP
                WHERE DEPTNO = :deptno
            """

            cursor.execute(sql,deptno=department_number)

        row = cursor.fetchone()

        return {
            "employee_count": row[0],
            "minimum_salary":
                float(row[1])
                if row[1] else None,
            "maximum_salary":
                float(row[2])
                if row[2] else None,
            "average_salary":
                float(row[3])
                if row[3] else None
        }

    finally:

        connection.close()


# ============================================================
# TOOL DEFINITIONS
# ============================================================
tools = [
    {
        "type": "function",
        "name": "get_department",
        "description": """
        Find an Oracle department by name.
        Returns department number, name and location.
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
        "name": "get_employees_by_department",
        "description": """
        Get employees for a department number.
        Returns employee information including salary.
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
        "name": "get_salary_statistics",

        "description": """
        Calculate salary statistics.
        If department_number is null,
        calculate statistics for all employees.
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
    }
]

# ============================================================
# TOOL DISPATCHER
# ============================================================
def execute_tool(name, arguments):
    if name == "get_department":
        return get_department(arguments["department_name"])
    elif name == "get_employees_by_department":
        return get_employees_by_department(arguments["department_number"])
    elif name == "get_salary_statistics":
        return get_salary_statistics(arguments["department_number"])
    else:
        raise ValueError(
            f"Unknown tool: {name}"
        )

# ============================================================
# AGENT
# ============================================================
def run_agent(user_question):
    response = client.responses.create(
        model="gpt-5",
        instructions="""
        You are an Oracle employee database assistant.
        You have access to the SCOTT schema.
        Use the available tools to retrieve information
        from the database.
        Never invent database information.
        If database information is required,
        use the appropriate tool.
        Explain the result clearly to the user.
        """,
        input=user_question,
        tools=tools
    )

    # ========================================================
    # AGENT LOOP
    # ========================================================
    while True:
        tool_outputs = []

        for item in response.output:
            if item.type != "function_call":
                continue
            print(f"\n[Agent selected tool: {item.name}]")
            print(f"[Arguments: {item.arguments}]")
            arguments = json.loads(item.arguments)
            result = execute_tool(item.name, arguments)
            print(f"[Tool result: {result}]")
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result)
            })
        # ----------------------------------------------------
        # No tools requested
        # ----------------------------------------------------
        if not tool_outputs:
            return response.output_text
        # ----------------------------------------------------
        # Send tool results back to GPT
        # ----------------------------------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )

# ============================================================
# CHAT LOOP
# ============================================================
while True:
    question = input("\nYou: ")
    if question.lower() in {
        "exit",
        "quit"
    }:
        break
    answer = run_agent(question)
    print("\nAI:", answer)