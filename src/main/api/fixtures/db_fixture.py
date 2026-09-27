import pytest
from sqlalchemy.orm import Session

from src.main.api.db.engine import SessionLocal, engine


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()