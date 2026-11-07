from fastapi.testclient import TestClient
from app.main import create_app
def test_route_cap():
    client = TestClient(create_app())
    assert client.post("/route", json={"prefer": "large", "max_cost": 0.001}).json()["provider"] == "local"
