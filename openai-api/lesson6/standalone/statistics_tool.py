
import os
import oracledb


def get_connection():

    return oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    )


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

            cursor.execute(
                sql,
                deptno=department_number
            )

        row = cursor.fetchone()

        return {
            "employee_count": row[0],
            "minimum_salary": float(row[1])
                if row[1] else None,
            "maximum_salary": float(row[2])
                if row[2] else None,
            "average_salary": float(row[3])
                if row[3] else None
        }

    finally:
        connection.close()
stats = get_salary_statistics()
for s in stats:
    print(s)