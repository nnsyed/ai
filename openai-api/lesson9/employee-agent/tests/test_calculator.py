from services.compensation_service import CompensationService


def test_seven_percent_raise():
    result = CompensationService.calculate(
        current_salary=2850,
        raise_percent=7,
        bonus_percent=0,
        fixed_bonus=0
    )

    assert (result["new_monthly_salary"] == 3049.50)


def test_raise_and_bonus():
    result = CompensationService.calculate(
        current_salary=2850,
        raise_percent=7,
        bonus_percent=10,
        fixed_bonus=0
    )

    assert (result["new_monthly_salary"] == 3049.50)
    assert (result["percentage_bonus"] == 304.95)


def test_fixed_bonus():
    result = CompensationService.calculate(
        current_salary=2850,
        raise_percent=0,
        bonus_percent=0,
        fixed_bonus=5000
    )

    assert (result["fixed_bonus"]== 5000)
