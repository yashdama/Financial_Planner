from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    debit_date: Mapped[date] = mapped_column(Date, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
                        CheckConstraint(
                        "amount_cents > 0",
                        name="ck_expenses_amount_cents_positive",
                    ),
    )
