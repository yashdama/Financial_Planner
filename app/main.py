from fastapi import FastAPI
from app.routers.calculations import router as calculations_router
from app.routers.expenses import expense_router

app = FastAPI()

app.include_router(
    calculations_router,
    prefix='/calculations',
    tags=['calculations']
)

app.include_router(
    expense_router,
    prefix='/expenses',
    tags=['expenses']
)

@app.get('/')
def health():
    return {
        'status': 'healthy',
        'application': 'financial_planner'}

