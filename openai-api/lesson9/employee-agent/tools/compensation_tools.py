from services.compensation_service import (CompensationService)

def calculate_compensation(current_salary, raise_percent=0, bonus_percent=0, fixed_bonus=0):
    return CompensationService.calculate(current_salary, raise_percent, bonus_percent, fixed_bonus)
