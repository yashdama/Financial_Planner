from tests.test_expenses_api import client

def test_monthly_summary(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.post("/monthly-summary",
            json={
                "year": 2026,
                "month": 9,
                "net_income_cents": 200000,
                "recurring_expenses_cents": [120000, 5000],
            },
        )
    assert response.status_code == 200
    body = response.json()
    assert body["year"] == 2026
    assert body["month"] == 9
    assert body["net_income_cents"] == 200000
    assert body["recurring_expenses_total_cents"] == 125000
    assert body["variable_expenses_total_cents"] == 128567
    assert body["monthly_surplus"] == -53567
    assert body["has_deficit"] is True

def test_monthly_summary_negative_recurring_expenses(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.post("/monthly-summary",
            json={
                "year": 2026,
                "month": 9,
                "net_income_cents": 200000,
                "recurring_expenses_cents": [-120000, 5000],
            },
        )
    assert response.status_code == 422

def test_monthly_summary_with_no_recurring_expenses(client):
    data = [{"name": "Groceries", "amount_cents": 8567, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 120000, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.post("/monthly-summary",
            json={
                "year": 2026,
                "month": 9,
                "net_income_cents": 200000,
                "recurring_expenses_cents": [],
            },
        )
    assert response.status_code == 200
    body = response.json()
    assert body["year"] == 2026
    assert body["month"] == 9
    assert body["net_income_cents"] == 200000
    assert body["recurring_expenses_total_cents"] == 0
    assert body["variable_expenses_total_cents"] == 128567
    assert body["monthly_surplus"] == 71433
    assert body["has_deficit"] is False

def test_monthly_summary_with_zero_expense_month(client):
    data = [{"name": "Groceries", "amount_cents": 0, "debit_date": "2026-09-10", "category": "food"},
            {"name": "Rent", "amount_cents": 0, "debit_date": "2026-09-12", "category": "housing"},
            {"name": "Utilities", "amount_cents": 5000, "debit_date": "2026-08-15", "category": "utilities"}]
    for expense in data:
        client.post("/expenses", 
                json=expense
            )

    response = client.post("/monthly-summary",
            json={
                "year": 2026,
                "month": 9,
                "net_income_cents": 200000,
                "recurring_expenses_cents": [120000],
            },
        )
    assert response.status_code == 200
    body = response.json()
    assert body["year"] == 2026
    assert body["month"] == 9
    assert body["net_income_cents"] == 200000
    assert body["recurring_expenses_total_cents"] == 120000
    assert body["variable_expenses_total_cents"] == 0
    assert body["monthly_surplus"] == 80000
    assert body["has_deficit"] is False
