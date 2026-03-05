import pytest
from fastapi.testclient import TestClient
from fraud_detection.serving.api import app

@pytest.fixture
def client():
    """Create a test client inside a context manager to trigger model loading."""
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint_logic(client):
    payload = {
        "transaction": {
            "transaction_id": "test-999",
            "timestamp": "2026-06-15T14:30:00",
            "amount": 100.0,
            "merchant_id": "m_1",
            "merchant_category": "grocery",
            "customer_id": "c_1",
            "customer_age": 30,
            "customer_country": "US",
            "card_type": "visa",
            "is_online": False,
            "is_foreign": False
        }
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "fraud_probability" in response.json()