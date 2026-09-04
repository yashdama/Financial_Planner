
def calculate_net_income(hourly_rate: int | float | None, 
                         monthly_salary: int | float | None, total_hours_worked:int | float | None, 
                         deductions: list[int | float]) -> float:
    
    total_deductions = 0

    use_hourly_rate = hourly_rate is not None
    use_monthly_salary = monthly_salary is not None

    if use_hourly_rate and hourly_rate < 0:
            raise ValueError('Hourly Rate cannot be negative')
    elif use_monthly_salary and monthly_salary < 0:
            raise ValueError('Monthly Salary cannot be negative')
    elif total_hours_worked is not None and total_hours_worked < 0 :
            raise ValueError('Hours worked cannot be negative')

    if use_hourly_rate == use_monthly_salary:
        raise ValueError('Please provide either hourly rate or monthly salary not both')

    if use_hourly_rate and total_hours_worked is None:
        raise ValueError('Provide total hours worked in a month if using hourly rate')
    
    for deduction in deductions:
        if deduction < 0:
            raise ValueError(f'Deductions {deduction} value is negative')
        total_deductions += deduction

    if use_hourly_rate:
        gross_income = hourly_rate * total_hours_worked
    else:
        gross_income = monthly_salary

    if total_deductions > gross_income:
        raise ValueError('Deductions cannot be greater than gross income')
    return float(gross_income - total_deductions)