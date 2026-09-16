import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.expense import Expense

@pytest.fixture
def client(tmp_path):
    database_file = tmp_path/"test.db"
    TEMP_DATABASE_URL = f"sqlite:///{database_file}"

    engine = create_engine(TEMP_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()

def test_create_expense(client):
    response = client.post(
        "/expenses",
        json={
            "name": "Groceries",
            "amount_cents": 8567,
            "debit_date": "2026-09-12",
            "category": "food",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Groceries"
    assert body["amount_cents"] == 8567
    assert body["debit_date"] == "2026-09-12"
    assert body["category"] == "food"
    assert body["created_at"] is not None

def test_create_expense_with_zero_amount_cents(client):
    response = client.post("/expenses",
            json={
                "name": "Groceries",
                "amount_cents": 0,
                "debit_date": "2026-09-12",
                "category": "food",
            },
        )
    assert response.status_code == 422

def test_get_expenses_endpoint(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.get("/expenses")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["name"] == "Rent"
    assert body[1]["name"] == "Groceries"

def test_get_expenses_with_query_params(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.get("/expenses?year=2026&month=9")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["name"] == "Rent"
    assert body[1]["name"] == "Groceries"

def test_get_expenses_with_query_params_incomplete(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.get("/expenses?year=2026")

    assert response.status_code == 422

def test_get_monthly_total_expenses(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]

    for expense_data in data:
        client.post('/expenses', json=expense_data)

    response = client.get('/expenses/monthly-total?year=2026&month=9')
    assert response.status_code == 200

    body = response.json()
    assert body['year'] == 2026
    assert body['month'] == 9
    assert body['total_amount_cents'] == 128567

def test_get_monthly_total_expenses_zero_expenses(client):
    data = [{"name": "Groceries", "amount_cents": 0, "debit_date": "2026-09-10", "category": "food"}]

    for expense_data in data:
        client.post('/expenses', json=expense_data)

    response = client.get('/expenses/monthly-total?year=2026&month=9')
    assert response.status_code == 200

    body = response.json()
    assert body['year'] == 2026
    assert body['month'] == 9
    assert body['total_amount_cents'] == 0

def test_get_monthly_total_expenses_december_month(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2025-12-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2025-12-31", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-01-01", "category": "utilities"}]
    

    for expense_data in data:
        client.post('/expenses', json=expense_data)

    response = client.get('/expenses/monthly-total?year=2025&month=12')
    assert response.status_code == 200

    body = response.json()
    assert body['year'] == 2025
    assert body['month'] == 12
    assert body['total_amount_cents'] == 128567

def test_get_monthly_total_expenses_missing_month(client):
    data = [
        {"name": "Groceries", "amount_cents": 8567, "debit_date": "2025-12-10", "category": "food"},
    ]
    

    for expense_data in data:
        client.post('/expenses', json=expense_data)

    response = client.get('/expenses/monthly-total?year=2025')
    assert response.status_code == 422

def test_get_expense_by_id(client):
    expense_data = {
        "name": "Gas",
        "amount_cents": 6000,
        "debit_date": "2026-09-14",
        "category": "utilites"
    }
    response = client.post("/expenses", json=expense_data)
    id = response.json()["id"]

    response_expense = client.get(f'expenses/{id}')
    assert response_expense.status_code == 200
    body = response_expense.json()

    assert body["id"] == id
    assert body["name"] == 'Gas'

def test_get_expense_by_id_invalid_id(client):
    response = client.get(f"/expenses/{999}")

    assert response.status_code == 404
    assert response.json() == {'detail': "Expense not found",}

def test_get_expense_by_id_zero(client):
    response = client.get(f"/expenses/{0}")

    assert response.status_code == 422

def test_update_expenses(client):
    expense_data = {'name': 'Electricity Bill',
                    'amount_cents': 4980,
                    'debit_date': '2026-09-14',
                    'category': 'utilities'}
    post_response = client.post('/expenses', json=expense_data)
    assert post_response.status_code == 201

    new_item_id = post_response.json()["id"]

    update_response = client.patch(f'expenses/{new_item_id}', json={'amount_cents': 498})
    assert update_response.status_code == 200
    assert update_response.json()['amount_cents'] == 498

    expense_response = client.get(f'expenses/{new_item_id}') 
    assert expense_response.status_code == 200

    assert expense_response.json()['amount_cents'] == 498
    assert expense_response.json()['name'] == 'Electricity Bill'
    assert expense_response.json()['category'] == 'utilities'

def test_update_expenses_none_values(client):
    expense_data = {'name': 'Electricity Bill',
                    'amount_cents': 4980,
                    'debit_date': '2026-09-14',
                    'category': 'utilities'}
    post_response = client.post('/expenses', json=expense_data)
    assert post_response.status_code == 201

    new_item_id = post_response.json()["id"]

    update_response = client.patch(f'expenses/{new_item_id}', json={})
    assert update_response.status_code == 422
    assert update_response.json()["detail"][0].get('msg') == 'Value error, Provide at least one field to update'

def test_delete_expense(client):
    expense_data = {'name': 'Electricity Bill',
                    'amount_cents': 4980,
                    'debit_date': '2026-09-14',
                    'category': 'utilities'}
    post_response = client.post('/expenses', json=expense_data)
    assert post_response.status_code == 201

    new_item_id = post_response.json()["id"]

    delete_response = client.delete(f'expenses/{new_item_id}')
    assert delete_response.status_code == 204

    get_response = client.get(f'/expenses/{new_item_id}')
    assert get_response.status_code == 404
