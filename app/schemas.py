from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date, datetime
from typing import Self

class ExpenseRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    amount_cents: int = Field(gt=0)
    debit_date: date
    category: str = Field(min_length=1, max_length=50)

class ExpenseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    amount_cents : int | None = Field(default=None, gt=0)
    debit_date: date | None = None
    category: str | None = Field(default=None, min_length=1, max_length=50)

    @model_validator(mode='after')
    def validate_update(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")

        for field_name in self.model_fields_set:
            if getattr(self, field_name) is None:
                raise ValueError(f"Field '{field_name}' cannot be None")

        return self

class NetIncomeRequest(BaseModel):
    hourly_rate: float | None = None
    monthly_salary: float | None = None
    total_hours_worked: float | None = None
    deductions: list[float] = Field(default_factory=list, description='Total Tax deductions')

class MonthlySurplusRequest(BaseModel):
    net_income: float
    recurring_expenses: list[float] = Field(default_factory=list, 
                                            description='Recurring expenses such as Rent, EMI')
    variable_expenses: list[float] = Field(default_factory=list, 
                                           description='Variable expenses such as groceries, gas')

class SavingsPlanRequest(BaseModel):
    current_savings: float
    goal_amount: float 
    target_months: int
    monthly_surplus: float

class ExpenseResponse(ExpenseRequest):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NetIncomeResponse(BaseModel):
    net_income: float = Field(..., description='Net Income after deductions')

class MonthlySurplusResponse(BaseModel):
    monthly_surplus: float = Field(..., description='Monthly surplus amount after expenses')

class SavingsPlanResponse(BaseModel):
    remaining_amount: float
    required_monthly_savings: float
    estimated_months: int | None
    achievable: bool
    monthly_shortfall: float
    monthly_cushion: float

class MonthlyExpenseResponse(BaseModel):
    year: int
    month: int
    total_amount_cents: int = Field(..., description='Total expenses for the specified month in cents')