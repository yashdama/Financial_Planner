from typing import Annotated
from datetime import date
from app.schemas import MonthlySummaryRequest, MonthlySummaryResponse
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select, func
from app.models.expense import Expense
from sqlalchemy.orm import Session
from app.database import get_db

summary_router = APIRouter()

@summary_router.post('', response_model=MonthlySummaryResponse)
def monthly_summary(income_data: MonthlySummaryRequest, 
                    db: Annotated[Session, Depends(get_db)]):
    
    year = income_data.year
    month = income_data.month

    start_date = date(year, month, 1)
    if month == 12:
        next_month_start_date = date(year + 1, 1, 1)
    else:
        next_month_start_date = date(year, month + 1, 1)

    recurring_expenses_total = sum(income_data.recurring_expenses_cents)

    query = select(func.sum(Expense.amount_cents)).where(
        Expense.debit_date >= start_date, 
        Expense.debit_date < next_month_start_date,
    )
    variable_expenses_total = db.scalar(query) or 0

    monthly_surplus = (income_data.net_income_cents - recurring_expenses_total - variable_expenses_total)

    return {'year': year,
            'month': month,
            'net_income_cents': income_data.net_income_cents,
            'recurring_expenses_total_cents': (recurring_expenses_total),
            'variable_expenses_total_cents': (variable_expenses_total),
            'monthly_surplus': monthly_surplus,
            'has_deficit': monthly_surplus < 0
            }