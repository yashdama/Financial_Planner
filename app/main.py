from fastapi import FastAPI
from fastapi import HTTPException
from app.schemas import NetIncomeResponse, NetIncomeRequest, MonthlySurplusRequest, MonthlySurplusResponse, SavingsPlanRequest, SavingsPlanResponse
from app.finance import calculate_net_income, calculate_monthly_surplus, calculate_savings_plan

app = FastAPI()

@app.get('/')
def health():
    return {
        'status': 'healthy',
        'application': 'financial_planner'}

@app.post('/calculations/net-income', response_model=NetIncomeResponse)
def calculate_net_income_endpoint(request: NetIncomeRequest):
    try:
        net_income = calculate_net_income(hourly_rate=request.hourly_rate,
                                      monthly_salary=request.monthly_salary,
                                      total_hours_worked=request.total_hours_worked,
                                      deductions=request.deductions)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return NetIncomeResponse(net_income=net_income)

@app.post('/calculations/monthly-surplus', response_model=MonthlySurplusResponse)
def calculate_monthly_surplus_endpoint(request: MonthlySurplusRequest):
    try:
        monthly_surplus = calculate_monthly_surplus(
            net_income=request.net_income, 
            recurring_expenses=request.recurring_expenses, 
            variable_expenses=request.variable_expenses)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return MonthlySurplusResponse(monthly_surplus=monthly_surplus)


@app.post('/calculations/savings-plan', response_model=SavingsPlanResponse)
def calculate_savings_plan_endpoint(request: SavingsPlanRequest):
    try:
        savings_plan = calculate_savings_plan(current_savings=request.current_savings,
                                              goal_amount=request.goal_amount, target_months=request.target_months,
                                              monthly_surplus=request.monthly_surplus)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return SavingsPlanResponse(**savings_plan)