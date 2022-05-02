from fastapi.testclient import TestClient
from main import app
from pg_database import DATABASE_URL

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200, 'Status code must be 200'


def test_create_user():
    response = client.post("/users/user")
    user_data = {
        'name': 'Ilon Mask',
        'email': 'tesla@spacer.com',
        'password': 'maskmask'
    }
    print(response.json())
    assert response.json() == user_data
    assert response.status_code == 201, 'Status code must be 201'

    #pytest tests
    #NOT Works perfect :(