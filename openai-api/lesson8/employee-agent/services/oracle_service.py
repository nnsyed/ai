import oracledb

from config import (
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_DSN
)

class OracleService:
    def __init__(self):
        self.user = ORACLE_USER
        self.password = ORACLE_PASSWORD
        self.dsn = ORACLE_DSN

    # ======================================================
    # Connection
    # ======================================================
    def get_connection(self):
        return oracledb.connect(user=self.user,password=self.password,dsn=self.dsn)

    # ======================================================
    # Employee
    # ======================================================
    def get_employee(self,employee_name):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT
                    EMPNO,
                    ENAME,
                    JOB,
                    MGR,
                    HIREDATE,
                    SAL,
                    COMM,
                    DEPTNO
                FROM EMP
                WHERE UPPER(ENAME) = UPPER(:name)
            """
            cursor.execute(sql,name=employee_name)
            row = cursor.fetchone()
            if row is None:
                return {
                    "found": False,
                    "message":"Employee not found"
                }
            return {
                "found": True,
                "employee_number": row[0],
                "name": row[1],
                "job": row[2],
                "manager_number": row[3],
                "hire_date": str(row[4]),
                "salary": float(row[5]),
                "commission":
                    float(row[6])
                    if row[6] is not None
                    else None,
                "department_number": row[7]
            }
        finally:
            connection.close()


    # ======================================================
    # Department
    # ======================================================
    def get_department(self,department_name):
        connection = self.get_connection()

        try:
            cursor = connection.cursor()
            sql = """
                SELECT
                    DEPTNO,
                    DNAME,
                    LOC
                FROM DEPT
                WHERE UPPER(DNAME) = UPPER(:name)
            """
            cursor.execute(sql,name=department_name)
            row = cursor.fetchone()
            if row is None:
                return {
                    "found": False,
                    "message":
                        "Department not found"
                }
            return {
                "found": True,
                "department_number": row[0],
                "department_name": row[1],
                "location": row[2]
            }
        finally:
            connection.close()

    # ======================================================
    # Employees
    # ======================================================
    def get_employees_by_department(self,department_number):
        connection = self.get_connection()
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
            cursor.execute(sql,deptno=department_number)
            employees = []
            for row in cursor:
                employees.append({
                    "employee_number": row[0],
                    "name": row[1],
                    "job": row[2],
                    "salary": float(row[3]),
                    "commission":
                        float(row[4])
                        if row[4] is not None
                        else None
                })
            return employees
        finally:
            connection.close()


    # ======================================================
    # Salary Statistics
    # ======================================================
    def get_salary_statistics(self, department_number=None):
        connection = self.get_connection()
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
                "employee_count":
                    row[0],
                "minimum_salary":
                    float(row[1]),
                "maximum_salary":
                    float(row[2]),
                "average_salary":
                    float(row[3])
            }
        finally:
            connection.close()
