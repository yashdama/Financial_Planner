from datetime import date
from typing import Annotated

from fastapi import (APIRouter, 
                     Depends, 
                     status, 
                     HTTPException, 
                     Path, 
                     Response,
                     Query)
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import (
    ExpenseRequest, 
    ExpenseResponse, 
    ExpenseUpdate, 
    MonthlyExpenseResponse)
from app.models.expense import Expense
from app.database import get_db

expense_router = APIRouter()

@expense_router.post('', response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense_data: ExpenseRequest, db: Annotated[Session, Depends(get_db)]):
    expense = Expense(**expense_data.model_dump())
    try:
        db.add(expense)
        db.commit()
        db.refresh(expense)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=422, detail="Expense violates a database constraint") from error

    return expense

@expense_router.get('', response_model=list[ExpenseResponse], status_code=status.HTTP_200_OK)
def get_expenses(db: Annotated[Session, Depends(get_db)], 
                 year: int | None = Query(default=None, ge=1, le=9998), 
                 month: int | None = Query(default=None, ge=1, le=12)):

    if (month is None) != (year is None):
        raise HTTPException(status_code=422, detail="Both 'year' and 'month' query parameters must be provided together")
    
    query = select(Expense)
    if year is not None and month is not None:
        start_date = date(year, month, 1)
        if month == 12:
            next_month_start = date(year + 1, 1, 1)
        else:
            next_month_start = date(year, month + 1, 1)
        query = query.where(Expense.debit_date >= start_date, Expense.debit_date < next_month_start)
    
    query = query.order_by(Expense.debit_date.desc(), 
                                     Expense.id.desc())

    return db.scalars(query).all()    

@expense_router.get('/monthly-total', response_model=MonthlyExpenseResponse, status_code=status.HTTP_200_OK)
def get_monthly_total_expenses(db: Annotated[Session, Depends(get_db)], 
                               year: int | None = Query(default=None, ge=1, le=9998),
                               month: int | None = Query(default=None, ge=1, le=12)):
    
    if year is None or month is None:
        raise HTTPException(status_code=422, detail='Provide both Month and Year to calculate Monthly total expenses')

    if year is not None and month is not None:
        start_date = date(year, month, 1)
        if month == 12:
            next_month_start = date(year + 1, 1, 1)
        else:
            next_month_start = date(year, month + 1, 1)

    query = select(func.sum(Expense.amount_cents)).where(Expense.debit_date >= start_date, Expense.debit_date < next_month_start)
    total_amount = db.scalar(query) or 0 

    return {"year": year, "month": month, "total_amount_cents": total_amount}

@expense_router.get('/{expense_id}', response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense(expense_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    expense = db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@expense_router.patch('/{expense_id}', response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense(expense_id: Annotated[int, Path(gt=0)], expense_data: ExpenseUpdate, db: Annotated[Session, Depends(get_db)]):
    expense_to_update = db.get(Expense, expense_id)
    if not expense_to_update:
        raise HTTPException(status_code=404, detail="Expense not found")
    try:
        changes = expense_data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(expense_to_update, field, value)
        db.commit()
        db.refresh(expense_to_update)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=422, detail="Expense violates a database constraint") from error

    return expense_to_update

@expense_router.delete('/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    expense_to_delete = db.get(Expense, expense_id)
    if not expense_to_delete:
        raise HTTPException(status_code=404, detail='Expense not found')
    try:
        db.delete(expense_to_delete)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=422, detail="Expense violates a database constraint") from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)

