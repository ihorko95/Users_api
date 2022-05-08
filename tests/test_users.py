import pytest
from httpx import AsyncClient
from main import app
from users.schemas import User
from users.main import create_user
from fastapi.testclient import TestClient


def test_users_list(temp_db):
    with TestClient(app) as client:
        response = client.get("/users/user-list")
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'user1', f'user from db'
    assert response.json()[0]['email'] == 'user1@gmail.com', f'user from db'
    assert response.json()[0]['id'] == 'uuid4-user1', f'user from db'


def test_create_user(temp_db):
    user = User(
        email="vaderqdw@deathstar.com",
        name="Darth",
        password="rainbow"
    )
    request_data = {
        "email": "vaderqdw@deathstar.com",
        "name": "Darth",
        "password": "rainbow"

    }
    with TestClient(app) as client:
        create_user(user)
        response = client.post(
            "users/user",
            json=request_data,

        )
    assert response.status_code == 201
    assert response.json()['name'] == request_data["name"], f'{response.json()["detail"][0]["msg"]}'
    assert response.json()['email'] == request_data["email"], f'{response.json()["detail"][0]["msg"]}'
