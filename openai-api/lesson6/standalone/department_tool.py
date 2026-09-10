import os
import oracledb


def get_connection():

    return oracledb.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"]
    )


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
            return {
                "found": False,
                "message": "Department not found"
            }

        return {
            "found": True,
            "department_number": row[0],
            "department_name": row[1],
            "location": row[2]
        }
    finally:
        connection.close()

result = get_department("SALES")
print(result)

