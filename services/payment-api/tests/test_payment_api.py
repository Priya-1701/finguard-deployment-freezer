from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FinGuard Payment API is running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "FinGuard Payment API"


def test_ready_endpoint():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_create_approved_payment():
    payload = {
        "amount": 999.50,
        "currency": "INR",
        "merchant_id": "merchant_001",
        "customer_id": "customer_001",
        "idempotency_key": "idem-test-001",
    }

    response = client.post("/pay", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "APPROVED"
    assert body["amount"] == 999.50
    assert body["currency"] == "INR"
    assert body["merchant_id"] == "merchant_001"
    assert "payment_id" in body


def test_create_declined_payment_for_large_amount():
    payload = {
        "amount": 200000.00,
        "currency": "INR",
        "merchant_id": "merchant_001",
        "customer_id": "customer_001",
    }

    response = client.post("/pay", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "DECLINED"


def test_payment_validation_rejects_negative_amount():
    payload = {
        "amount": -10,
        "currency": "INR",
        "merchant_id": "merchant_001",
        "customer_id": "customer_001",
    }

    response = client.post("/pay", json=payload)

    assert response.status_code == 422


def test_get_missing_payment_returns_404():
    response = client.get("/payments/not-a-real-payment-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_simulated_error_endpoint():
    response = client.get("/simulate/error")

    assert response.status_code == 500
    assert response.json()["detail"] == "Simulated payment API failure"


def test_simulated_latency_endpoint():
    response = client.get("/simulate/latency?delay_ms=1")

    assert response.status_code == 200
    assert response.json()["delay_ms"] == 1


def test_metrics_endpoint_exposes_prometheus_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "finguard_http_requests_total" in response.text
    assert "finguard_payment_requests_total" in response.text
