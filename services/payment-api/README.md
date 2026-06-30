# Payment API


The Payment API is the first core microservice in the FinGuard Deployment Freezer project.

It simulates a fintech payment authorization service and produces reliability signals that will later be used for SLOs, error-budget checks, canary validation, rollback decisions, and deployment freeze logic.

Current Phase Status

Completed so far:

Phase 1: Built FastAPI Payment API
Phase 2: Dockerized the Payment API
Phase 3: Added PostgreSQL persistence and ledger entries
Features Implemented
FastAPI-based payment service
Health endpoint
Readiness endpoint
Payment creation endpoint
Payment lookup endpoint
Payment ledger lookup endpoint
Database health endpoint
Failure simulation endpoint
Latency simulation endpoint
Prometheus metrics endpoint
Dockerfile
Docker Compose setup
PostgreSQL integration
SQLAlchemy ORM models
Pytest test coverage
Trivy image scan workflow
Endpoints
Method	Endpoint	Purpose
GET	/	Service information
GET	/health	API health check
GET	/ready	API readiness check
GET	/db/health	Database connectivity check
POST	/pay	Create a payment
GET	/payments/{payment_id}	Fetch payment by ID
GET	/payments/{payment_id}/ledger	Fetch payment with ledger entries
GET	/simulate/error	Simulate HTTP 500 error
GET	/simulate/latency?delay_ms=1000	Simulate slow API response
GET	/metrics	Prometheus metrics
Database Tables
payment_transactions

Stores payment decisions.

Main fields:

payment_id
status
amount
currency
merchant_id
customer_id
idempotency_key
message
created_at
ledger_entries

Stores accounting-style ledger records for approved payments.

Approved payments create:

DEBIT_CUSTOMER
CREDIT_MERCHANT

Declined payments are stored, but no ledger entries are created.

Run Locally with Python

From project root:

cd ~/Projects/finguard-deployment-freezer
source .venv/bin/activate
cd services/payment-api
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Test health:

curl -s http://127.0.0.1:8000/health | jq
Run with Docker Compose

From project root:

cd ~/Projects/finguard-deployment-freezer
make payment-api-compose-up

Check API health:

make payment-api-health

Check database health:

make payment-api-db-health

Stop services:

make payment-api-compose-down

Reset database completely:

make payment-api-compose-reset
Example Payment Request
curl -s -X POST http://127.0.0.1:8000/pay \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2499.75,
    "currency": "INR",
    "merchant_id": "merchant_001",
    "customer_id": "customer_001",
    "idempotency_key": "order-001"
  }' | jq
Example Ledger Lookup
PAYMENT_ID=$(curl -s -X POST http://127.0.0.1:8000/pay \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 3500,
    "currency": "INR",
    "merchant_id": "merchant_002",
    "customer_id": "customer_002",
    "idempotency_key": "order-002"
  }' | jq -r '.payment.payment_id')

curl -s http://127.0.0.1:8000/payments/$PAYMENT_ID/ledger | jq
Run Tests

From project root:

cd ~/Projects/finguard-deployment-freezer
source .venv/bin/activate
pytest
Docker Image Build
make payment-api-docker-build
Trivy Scan
make payment-api-trivy-scan
Metrics Exposed
Metric	Purpose
finguard_http_requests_total	Total HTTP requests by method, path, and status
finguard_http_request_duration_seconds	API request latency
finguard_payment_requests_total	Payment count by status
finguard_payment_amount_total	Approved payment amount by currency
finguard_payment_errors_total	API error count by type
finguard_payment_store_size	Total persisted payments
Why This Service Matters

This service is the base application used by FinGuard Deployment Freezer.

It provides real signals such as:

API health
Database health
Payment success/failure
Latency
Error rate
Prometheus metrics
Persistent transaction data
Ledger records

These signals will later help decide whether a deployment should continue, pause, roll back, or freeze.
