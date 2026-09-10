from fastapi import FastAPI
from app.routers.calculations import router as calculations_router

app = FastAPI()

app.include_router(
    calculations_router,
    prefix='/calculations',
    tags=['calculations']
)

@app.get('/')
def health():
    return {
        'status': 'healthy',
        'application': 'financial_planner'}

