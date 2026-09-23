class CompensationService:
    @staticmethod
    def calculate(current_salary, raise_percent=0, bonus_percent=0, fixed_bonus=0):

        # --------------------------------------------------
        # Raise
        # --------------------------------------------------
        raise_amount = (
            current_salary *
            raise_percent /
            100
        )

        new_salary = (
            current_salary +
            raise_amount
        )

        # --------------------------------------------------
        # Bonus
        # --------------------------------------------------
        percentage_bonus = (
            new_salary *
            bonus_percent /
            100
        )

        total_bonus = (
            percentage_bonus +
            fixed_bonus
        )


        # --------------------------------------------------
        # Annual salary
        # --------------------------------------------------

        annual_base = (
            new_salary * 12
        )

        annual_compensation = (
            annual_base +
            total_bonus
        )

        return {
            "current_monthly_salary":
                round(current_salary, 2),
            "raise_percent":
                raise_percent,
            "raise_amount":
                round(raise_amount, 2),
            "new_monthly_salary":
                round(new_salary, 2),
            "bonus_percent":
                bonus_percent,
            "percentage_bonus":
                round(
                    percentage_bonus,
                    2
                ),
            "fixed_bonus":
                round(
                    fixed_bonus,
                    2
                ),
            "total_bonus":
                round(
                    total_bonus,
                    2
                ),
            "annual_base_salary":
                round(
                    annual_base,
                    2
                ),
            "total_annual_compensation":
                round(
                    annual_compensation,
                    2
                )
        }