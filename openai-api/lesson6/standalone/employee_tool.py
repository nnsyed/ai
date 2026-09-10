import os
import oracledb


def get_connection():

    return oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    )

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
                "salary": float(row[3]) if row[3] else None,
                "commission": float(row[4])
                    if row[4] else None
            })

        return employees

    finally:
        connection.close()

employees = get_employees_by_department(30)
for employee in employees:
    print(employee)