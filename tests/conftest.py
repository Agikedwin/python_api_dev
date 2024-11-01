from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings
from app.auth2 import create_access_token
from app import models

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


@pytest.fixture
def test_user(client):
    user_data ={"email": "agikedwin3@gmail.com", "password": "admin"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data ={"email": "agikedwin34@gmail.com", "password": "admin"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return  create_access_token({"user_id":test_user['id']})
@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_create_post(test_user, session, test_user2):
    post_data = [
        {
            "title": "test title",
            "content": "test content",
            "owner_id": test_user['id']

        },
        {
            "title": "test title 1",
            "content": "test content 1",
            "owner_id": test_user['id']

        },
        {
            "title": "test title 2",
            "content": "test content 2",
            "owner_id": test_user['id']

        },
        {
            "title": "test title auth",
            "content": "test content auth",
            "owner_id": test_user2['id']

        }
    ]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    post_list = list(post_map)
    session.add_all(post_list)

    #OR
    # session.add_all([models.Post(
    #     title= "test title",
    #     content= "test content",
    #     owner_id = test_user['id']
    # ),models.Post(
    #     title= "test title 1",
    #     content= "test content 1",
    #     owner_id = test_user['id']
    # ),models.Post(
    #     title= "test title 2",
    #     content= "test content 2",
    #     owner_id = test_user['id']
    # )])

    session.commit()
    post_res = session.query(models.Post).all()
    return post_res



