from services.oracle_service import OracleService

oracle = OracleService()

def get_employee(employee_name):
    return oracle.get_employee(employee_name)

def get_department(department_name):
    return oracle.get_department(department_name)

def get_employees_by_department(department_number):
    return oracle.get_employees_by_department(department_number)

def get_salary_statistics(department_number=None):
    return oracle.get_salary_statistics(department_number)