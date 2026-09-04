
import pytest
from app.finance import calculate_net_income

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
            match='Deductions cannot be greater than gross income',
        ):
            calculate_net_income(hourly_rate=50, monthly_salary=None, total_hours_worked=0, deductions=[1000])

