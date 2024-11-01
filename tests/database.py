from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings

URL_DATABASE = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=30)

TestingSessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Before the test run, drop our tables
    Base.metadata.drop_all(bind=engine)
    # After the tests run, create tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


