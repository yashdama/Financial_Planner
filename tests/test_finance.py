
import pytest, math
from app.finance import calculate_net_income, calculate_monthly_surplus, calculate_savings_plan

def test_calculate_net_income_hourly():
    assert calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=160, deductions=[1000]) == 7000.0

def test_calculate_net_income_monthly():
    assert calculate_net_income(hourly_rate=None, monthly_salary=8000, total_hours_worked=None, deductions=[1000]) == 7000.0

def test_calculate_net_income_no_deductions():
    assert calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=160, deductions=[]) == 8000.0

def test_calculate_net_income_negative_hourly_rate():
    with pytest.raises(
        ValueError,
        match="Hourly Rate cannot be negative",
    ):
        calculate_net_income(
            hourly_rate=-50,
            monthly_salary=None,
            total_hours_worked=160,
            deductions=[1000],
        )

def test_calculate_net_income_negative_monthly_salary():
    with pytest.raises(
        ValueError,
        match="Monthly Salary cannot be negative",
    ):
        calculate_net_income(
            hourly_rate=None,
            monthly_salary=-8000,
            total_hours_worked=None,
            deductions=[1000],
        )

def test_calculate_net_income_negative_hours_worked():
    try:
        calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=-160, deductions=[1000])
    except ValueError as e:
        assert str(e) == 'Hours worked cannot be negative'

def test_calculate_net_income_negative_deduction():
    try:
        calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=160, deductions=[-1000])
    except ValueError as e:
        assert str(e) == 'Deductions -1000 value is negative'

def test_calculate_net_income_multiple_deductions():
    assert calculate_net_income(hourly_rate=None, monthly_salary=8000, total_hours_worked = None, deductions=[1000, 500, 200]) == 6300.0

def test_calculate_net_income_without_salary_type_provided():
    with pytest.raises(
        ValueError,
        match='Please provide either hourly rate or monthly salary not both',
    ):
        calculate_net_income(hourly_rate=None, monthly_salary=None, total_hours_worked=160, deductions=[1000])

def test_calculate_net_income_with_both_salary_types_provided():
    with pytest.raises(
        ValueError,
        match='Please provide either hourly rate or monthly salary not both',
    ):
        calculate_net_income(hourly_rate=50, monthly_salary=8000, total_hours_worked=160, deductions=[1000])

def test_calculate_net_income_with_hourly_rate_without_hours_worked():
    with pytest.raises(
        ValueError,
        match='Provide total hours worked in a month if using hourly rate',
    ):
        calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=None, deductions=[1000])

def test_calculate_net_income_zero_hours_worked():
    with pytest.raises(
            ValueError,
            match='Provide total hours worked in a month if using hourly rate',
        ):
            calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=0, deductions=[1000])

def test_calculate_monthly_surplus_negative_net_income():
    with pytest.raises(
        ValueError,
        match='Net Income cannot be negative'
    ):
        calculate_monthly_surplus(net_income=-1000, recurring_expenses=[], variable_expenses=[])

def test_calculate_monthly_surplus_negative_recurring_expenses():
    with pytest.raises(
        ValueError,
        match='Recurring expenses cannot be negative'
    ):
        calculate_monthly_surplus(net_income=1000, recurring_expenses=[-500, 100], variable_expenses=[200, 300])

def test_calculate_monthly_surplus_negative_variable_expenses():
    with pytest.raises(
        ValueError,
        match='Variable expenses cannot be negative'
    ):
        calculate_monthly_surplus(net_income=1000, recurring_expenses=[500, 100], variable_expenses=[-200, 300])

def test_calculate_monthly_surplus_empty_lists():
    assert calculate_monthly_surplus(net_income=1000, recurring_expenses=[], variable_expenses=[]) == 1000.0

def test_calculate_montly_surplus_zero():
    assert calculate_monthly_surplus(net_income=3000, recurring_expenses=[1000, 500], variable_expenses=[500, 1000]) == 0.0

def test_calculate_monthy_surplus_negative_surplus():
    assert calculate_monthly_surplus(net_income=1000, recurring_expenses=[500, 100], variable_expenses=[200, 300]) == -100.0

def test_calculate_monthly_surplus_positive_surplus():
    assert calculate_monthly_surplus(net_income=6000, recurring_expenses=[1000, 500], variable_expenses=[1000, 500]) == 3000.0

def test_calculate_savings_plan_expenses():
    assert calculate_savings_plan(current_savings=1000, goal_amount=5000, target_months=10, monthly_surplus=500) == {
        'remaining_amount': 4000.0,
        'required_monthly_savings': 400.0,
        'estimated_months': 8,
        'achievable': True,
        'monthly_shortfall': 0.0,
        'monthly_cushion': 100
    }

def test_calculate_savings_plan_estimated_months_None():
    assert calculate_savings_plan(current_savings=10000, goal_amount=100000, target_months=36, monthly_surplus=0) == {
        'remaining_amount': 90000.0,
        'required_monthly_savings': 2500.0,
        'estimated_months': None,
        'achievable': False,
        'monthly_shortfall': 2500.0,
        'monthly_cushion': 0
    }

def test_calculate_savings_plan_estimated_months_None_shortfall_3000():
    assert calculate_savings_plan(current_savings=10000, goal_amount=100000, target_months=36, monthly_surplus=-500) == {
        'remaining_amount': 90000.0,
        'required_monthly_savings': 2500.0,
        'estimated_months': None,
        'achievable': False,
        'monthly_shortfall': 3000.0,
        'monthly_cushion': 0
    }

def test_calculate_savings_plan_estimated_months_valueerror():
    with pytest.raises(
        ValueError,
        match='Target months must be greater than zero'
    ):
        calculate_savings_plan(current_savings=100000, goal_amount=100000, target_months=0, monthly_surplus=2000)