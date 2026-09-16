from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from collections.abc import Generator
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

DATABASE_URL = "sqlite:///./financial_planner.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()