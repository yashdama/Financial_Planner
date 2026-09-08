import math

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

def calculate_monthly_surplus(net_income: float, recurring_expenses: list[int | float], 
                              variable_expenses: list[int | float]) -> float:
    if net_income < 0:
        raise ValueError('Net Income cannot be negative')

    total_recurring_expenses = 0
    total_variable_expenses = 0

    for expense in recurring_expenses:
        if expense < 0:
            raise ValueError('Recurring expenses cannot be negative')
        total_recurring_expenses += expense
    
    for expense in variable_expenses:
        if expense < 0:
            raise ValueError('Variable expenses cannot be negative')
        total_variable_expenses += expense

    return float(net_income - total_recurring_expenses - total_variable_expenses)

def calculate_savings_plan(current_savings: float, goal_amount: float, target_months : int, monthly_surplus: float) -> dict:

    if goal_amount <= 0:
        raise ValueError('Goal Amount must be greater than zero')

    if current_savings < 0:
        raise ValueError('Current saving cannot be negative, if no savings zero is accepted')

    if target_months <= 0:
        raise ValueError('Target months must be greater than zero')

    remaining_amount = max(0, goal_amount - current_savings)

    if remaining_amount == 0:
        return {'remaining_amount': remaining_amount, 
                'required_monthly_savings': 0.0,
                'estimated_months': 0,
                'achievable': True,
                'monthly_shortfall': 0.0,
                'monthly_cushion': 0.0
                }

    required_monthly_savings = remaining_amount / target_months

    if monthly_surplus <= 0:
        estimated_months = None
    else:
        estimated_months = math.ceil(remaining_amount / monthly_surplus)

    achievable = monthly_surplus >= required_monthly_savings

    monthly_shortfall = max(0, required_monthly_savings - monthly_surplus)

    monthly_cushion = max(0, monthly_surplus - required_monthly_savings)

    return {'remaining_amount': remaining_amount, 
            'required_monthly_savings': required_monthly_savings,
            'estimated_months': estimated_months,
            'achievable': achievable,
            'monthly_shortfall': monthly_shortfall,
            'monthly_cushion': monthly_cushion
            }

