import pytest
from app import schemas
from app.config import settings

from jose import jwt

def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    assert res.json().get('message') == 'This is a default message'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "agikedwin3@gmail.com", "password": "admin"})

    new_user = schemas.UserResponse(**res.json())
    assert res.json().get("email") == 'agikedwin3@gmail.com'
    #OR
    assert new_user.email == 'agikedwin3@gmail.com'
    assert res.status_code == 201

def test_login_user(client, test_user ):
    res = client.post("/login/", data={"username": test_user['email'], "password":test_user['password']})

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
    ('agikedwinwrong@gmail.com','admin',403),
    ('agikedwin3@gmail.com','adminwrong',403),
    ('agikedwin3wrong@gmail.com','adminwrong',403),
    (None,'admin',422),
    ('agikedwin@gmail.com',None,422)
])
def test_incorrect_login(test_user, client,email,password,status_code):
    res = client.post('/login', data={"username":email, "password":password})
    assert res.status_code == status_code
