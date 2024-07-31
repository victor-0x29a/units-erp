from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_world():
    response = client.get("/hello_world")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
