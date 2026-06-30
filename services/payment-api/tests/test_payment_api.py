import os
from pathlib import Path

TEST_DB_PATH = Path("test_payment_api.db")
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

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
    assert body["environment"] == "test"


def test_ready_endpoint():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_database_health_endpoint():
    response = client.get("/db/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["database"] == "sqlite"


def test_create_approved_payment_with_ledger_entries():
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

    assert body["payment"]["status"] == "APPROVED"
    assert body["payment"]["amount"] == 999.50
    assert body["payment"]["currency"] == "INR"
    assert body["payment"]["merchant_id"] == "merchant_001"
    assert "payment_id" in body["payment"]

    assert len(body["ledger_entries"]) == 2
    assert body["ledger_entries"][0]["entry_type"] == "DEBIT_CUSTOMER"
    assert body["ledger_entries"][1]["entry_type"] == "CREDIT_MERCHANT"


def test_fetch_payment_and_ledger_by_payment_id():
    payload = {
        "amount": 1500,
        "currency": "INR",
        "merchant_id": "merchant_ledger_001",
        "customer_id": "customer_ledger_001",
    }

    create_response = client.post("/pay", json=payload)
    payment_id = create_response.json()["payment"]["payment_id"]

    payment_response = client.get(f"/payments/{payment_id}")
    assert payment_response.status_code == 200
    assert payment_response.json()["payment_id"] == payment_id

    ledger_response = client.get(f"/payments/{payment_id}/ledger")
    assert ledger_response.status_code == 200
    assert ledger_response.json()["payment"]["payment_id"] == payment_id
    assert len(ledger_response.json()["ledger_entries"]) == 2


def test_create_declined_payment_has_no_ledger_entries():
    payload = {
        "amount": 200000.00,
        "currency": "INR",
        "merchant_id": "merchant_001",
        "customer_id": "customer_001",
    }

    response = client.post("/pay", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["payment"]["status"] == "DECLINED"
    assert body["ledger_entries"] == []


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


def test_get_missing_payment_ledger_returns_404():
    response = client.get("/payments/not-a-real-payment-id/ledger")

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
