'''
New salary = Current salary + Salary increase
Total compensation = New salary + Bonus

'''


def calculate_compensation(current_salary,raise_percent=0,bonus_percent=0,fixed_bonus=0):
    # ------------------------------------------------------
    # Calculate raise
    # ------------------------------------------------------
    raise_amount=(current_salary*raise_percent /100)
    new_salary=(current_salary + raise_amount)

    # ------------------------------------------------------
    # Calculate percentage bonus
    # ------------------------------------------------------
    percentage_bonus=(new_salary * bonus_percent/100)

    # ------------------------------------------------------
    # Total bonus
    # ------------------------------------------------------
    total_bonus=(percentage_bonus+fixed_bonus)

    # ------------------------------------------------------
    # Annual compensation
    # ------------------------------------------------------
    annual_base_salary=(new_salary * 12)
    total_annual_compensation=(annual_base_salary + total_bonus)

    # ------------------------------------------------------
    # Monthly equivalent
    # ------------------------------------------------------
    monthly_total_compensation=(total_annual_compensation / 12)
    return {
        "current_monthly_salary":round(current_salary, 2),
        "raise_percent":raise_percent,
        "raise_amount":round(raise_amount, 2),
        "new_monthly_salary":round(new_salary, 2),
        "bonus_percent":bonus_percent,
        "percentage_bonus":round(percentage_bonus, 2),
        "fixed_bonus":round(fixed_bonus, 2),
        "total_bonus":round(total_bonus, 2),
        "annual_base_salary":round(annual_base_salary, 2),
        "total_annual_compensation":round(total_annual_compensation,2),
        "monthly_total_compensation":round(monthly_total_compensation,2)
    }

def convert_currency(amount,exchange_rate):
    converted_amount = (amount * exchange_rate)
    return { 
        "original_amount": round(amount, 2),
        "exchange_rate": exchange_rate,
        "converted_amount": round(converted_amount, 2)
    }
