from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy', 'application': 'financial_planner'}

def test_calculate_net_income_endpoint():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': 20.0,
        'monthly_salary': None,
        'total_hours_worked': 160.0,
        'deductions': [200.0, 150.0]
    })
    assert response.status_code == 200
    assert response.json() == {'net_income': 2850.0}

def test_calculate_net_income_endpoint_invalid_input():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': 20.0,
        'monthly_salary': 2000.0,
        'total_hours_worked': 160.0,
        'deductions': [200.0, 150.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Please provide either hourly rate or monthly salary not both'

def test_calculate_net_income_endpoint_missing_hours():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': 20.0,
        'monthly_salary': None,
        'total_hours_worked': 0.0,
        'deductions': [200.0, 150.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Provide total hours worked in a month if using hourly rate'

def test_calculate_net_income_endpoint_missing_input():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': None,
        'monthly_salary': None,
        'total_hours_worked': 0.0,
        'deductions': [200.0, 150.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Please provide either hourly rate or monthly salary not both'

def test_calculate_net_income_endpoint_deductions_greater_than_salary():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': 50,
        'monthly_salary': None,
        'total_hours_worked': 100.0,
        'deductions': [3000.0, 3000.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Deductions cannot be greater than gross income'

def test_calculate_net_income_endpoint_negative_deductions():
    response = client.post('/calculations/net-income', json={
        'hourly_rate': 50,
        'monthly_salary': None,
        'total_hours_worked': 100.0,
        'deductions': [-3000.0, 1500.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Deductions -3000.0 value is negative'

def test_calculate_monthly_surplus_endpoint():
    response = client.post('/calculations/monthly-surplus', json={
        'net_income': 3000.0,
        'recurring_expenses': [1000.0, 500.0],
        'variable_expenses': [200.0, 300.0]
    })
    assert response.status_code == 200
    assert response.json() == {'monthly_surplus': 1000.0}

def test_calculate_monthly_surplus_endpoint_negative_net_income():
    response = client.post('/calculations/monthly-surplus', json={
        'net_income': -3000.0,
        'recurring_expenses': [1000.0, 500.0],
        'variable_expenses': [200.0, 300.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Net Income cannot be negative'

def test_calculate_monthly_surplus_endpoint_negative_recurring_expenses():
    response = client.post('/calculations/monthly-surplus', json={
        'net_income': 3000.0,
        'recurring_expenses': [-1000.0, 500.0],
        'variable_expenses': [200.0, 300.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Recurring expenses cannot be negative'

def test_calculate_monthly_surplus_endpoint_negative_variable_expenses():
    response = client.post('/calculations/monthly-surplus', json={
        'net_income': 3000.0,
        'recurring_expenses': [1000.0, 500.0],
        'variable_expenses': [-200.0, 300.0]
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Variable expenses cannot be negative'

def test_calculate_savings_plan_endpoint():
    response = client.post('/calculations/savings-plan', json={
        'current_savings': 5000.0,
        'goal_amount': 20000.0,
        'target_months': 12,
        'monthly_surplus': 1000.0
    })
    assert response.status_code == 200
    assert response.json() == {
        'remaining_amount': 15000.0,
        'required_monthly_savings': 1250.0,
        'estimated_months': 15,
        'achievable': False,
        'monthly_shortfall': 250.0,
        'monthly_cushion': 0.0
    }

def test_calculate_savings_plan_endpoint_zero_goal_amount():
    response = client.post('/calculations/savings-plan', json={
        'current_savings': 5000.0,
        'goal_amount': 0.0,
        'target_months': 12,
        'monthly_surplus': 1000.0
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Goal Amount must be greater than zero'

def test_calculate_savings_plan_endpoint_negative_current_savings():
    response = client.post('/calculations/savings-plan', json={
        'current_savings': -5000.0,
        'goal_amount': 20000.0,
        'target_months': 12,
        'monthly_surplus': 1000.0
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Current savings cannot be negative, if no savings zero is accepted'

def test_calculate_savings_plan_endpoint_zero_target_months():
    response = client.post('/calculations/savings-plan', json={
        'current_savings': 5000.0,
        'goal_amount': 20000.0,
        'target_months': 0,
        'monthly_surplus': 1000.0
    })
    assert response.status_code == 422
    print(response.json())
    assert response.json()['detail'] == 'Target months must be greater than zero'

def test_calculate_savings_plan_endpoint_negative_monthly_surplus():
    response = client.post('/calculations/savings-plan', json={
        'current_savings': 5000.0,
        'goal_amount': 20000.0,
        'target_months': 12,
        'monthly_surplus': -1000.0
    })
    assert response.status_code == 200
    assert response.json() == {
        'remaining_amount': 15000.0,
        'required_monthly_savings': 1250.0,
        'estimated_months': None,
        'achievable': False,
        'monthly_shortfall': 2250.0,
        'monthly_cushion': 0.0
    }

