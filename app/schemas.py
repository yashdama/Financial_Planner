from pydantic import BaseModel, Field

class NetIncomeRequest(BaseModel):
    hourly_rate: float | None = None
    monthly_salary: float | None = None
    total_hours_worked: float | None = None
    deductions: list[float] = Field(default_factory=list, description='Total Tax deductions')

class MonthlySurplusRequest(BaseModel):
    net_income: float | None = None
    recurring_expenses: list[float] = Field(default_factory=list, 
                                            description='Recurring expenses such as Rent, EMI')
    variable_expenses: list[float] = Field(default_factory=list, 
                                           description='Variable expenses such as groceries, gas')

class SavingsPlanRequest(BaseModel):
    current_savings: float | None = None
    goal_amount: float | None = None
    target_months: int | None = None
    monthly_surplus: float | None = None

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

