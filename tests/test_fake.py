from fastapi.testclient import TestClient


def test_fake_customers(client: TestClient):
    response = client.get("/fake?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_parcels(client: TestClient):
    response = client.get("/fake/packages?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
