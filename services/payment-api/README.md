# FinGuard Payment API

Production-style fintech payment service for the **FinGuard Deployment Freezer** project.

This service simulates a real payment authorization system and generates reliability signals that will later be used for SLO checks, error-budget decisions, canary validation, rollback automation, and deployment freeze logic.

---

## What We Have Built So Far

The Payment API currently includes:

* FastAPI-based payment service
* Dockerized runtime
* Docker Compose local stack
* PostgreSQL-backed payment persistence
* Ledger entry creation for approved payments
* Database health checks
* Prometheus metrics
* Failure and latency simulation
* Pytest-based API validation
* Trivy image scanning workflow

---

## Service Architecture

```text
Client / curl / k6
      |
      v
FastAPI Payment API
      |
      |-- /health
      |-- /ready
      |-- /db/health
      |-- /pay
      |-- /payments/{payment_id}
      |-- /payments/{payment_id}/ledger
      |-- /simulate/error
      |-- /simulate/latency
      |-- /metrics
      |
      v
PostgreSQL
      |
      |-- payment_transactions
      |-- ledger_entries
```

---

## Tech Stack Used

| Area                        | Tool                     |
| --------------------------- | ------------------------ |
| API Framework               | FastAPI                  |
| Language                    | Python                   |
| Database                    | PostgreSQL               |
| ORM                         | SQLAlchemy               |
| Containerization            | Docker                   |
| Local Multi-Service Runtime | Docker Compose           |
| Metrics                     | Prometheus Python Client |
| Testing                     | Pytest                   |
| Security Scan               | Trivy                    |

---

## API Endpoints

| Method | Endpoint                          | Purpose                           |
| ------ | --------------------------------- | --------------------------------- |
| GET    | `/`                               | Service information               |
| GET    | `/health`                         | API liveness check                |
| GET    | `/ready`                          | API readiness check               |
| GET    | `/db/health`                      | Database connectivity check       |
| POST   | `/pay`                            | Create a payment transaction      |
| GET    | `/payments/{payment_id}`          | Fetch payment details             |
| GET    | `/payments/{payment_id}/ledger`   | Fetch payment with ledger entries |
| GET    | `/simulate/error`                 | Simulate API failure              |
| GET    | `/simulate/latency?delay_ms=1000` | Simulate slow response            |
| GET    | `/metrics`                        | Prometheus metrics endpoint       |

---

## Database Design

### `payment_transactions`

Stores the final payment decision.

| Field             | Purpose                                |
| ----------------- | -------------------------------------- |
| `payment_id`      | Unique payment identifier              |
| `status`          | `APPROVED` or `DECLINED`               |
| `amount`          | Payment amount                         |
| `currency`        | Payment currency                       |
| `merchant_id`     | Merchant receiving payment             |
| `customer_id`     | Customer making payment                |
| `idempotency_key` | Duplicate request protection reference |
| `message`         | Payment decision message               |
| `created_at`      | Transaction timestamp                  |

### `ledger_entries`

Stores accounting-style ledger records for approved payments.

For every approved payment, two ledger entries are created:

```text
DEBIT_CUSTOMER
CREDIT_MERCHANT
```

Declined payments are saved in `payment_transactions`, but no ledger movement is created.

---

## Run the Service with Docker Compose

From the project root:

```bash
cd ~/Projects/finguard-deployment-freezer
make payment-api-compose-up
```

Check API health:

```bash
make payment-api-health
```

Check database health:

```bash
make payment-api-db-health
```

Stop the stack:

```bash
make payment-api-compose-down
```

Reset the database completely:

```bash
make payment-api-compose-reset
```

---

## Create a Payment

```bash
curl -s -X POST http://127.0.0.1:8000/pay \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2499.75,
    "currency": "INR",
    "merchant_id": "merchant_001",
    "customer_id": "customer_001",
    "idempotency_key": "order-001"
  }' | jq
```

Expected result:

```json
{
  "payment": {
    "status": "APPROVED",
    "message": "Payment approved"
  },
  "ledger_entries": [
    {
      "entry_type": "DEBIT_CUSTOMER"
    },
    {
      "entry_type": "CREDIT_MERCHANT"
    }
  ]
}
```

---

## Fetch Payment Ledger

```bash
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
```

---

## Verify Data in PostgreSQL

Open the database shell:

```bash
make payment-api-db-shell
```

List tables:

```sql
\dt
```

Check recent payments:

```sql
SELECT payment_id, status, amount, currency, merchant_id, customer_id, created_at
FROM payment_transactions
ORDER BY created_at DESC
LIMIT 5;
```

Check ledger entries:

```sql
SELECT ledger_entry_id, payment_id, entry_type, account_ref, amount, currency
FROM ledger_entries
ORDER BY created_at DESC
LIMIT 10;
```

Exit PostgreSQL:

```sql
\q
```

---

## Run Tests

From the project root:

```bash
cd ~/Projects/finguard-deployment-freezer
source .venv/bin/activate
pytest
```

---

## Build Docker Image

```bash
make payment-api-docker-build
```

---

## Run Trivy Scan

```bash
make payment-api-trivy-scan
```

---

## Prometheus Metrics

The service exposes metrics at:

```text
/metrics
```

Important metrics:

| Metric                                   | Purpose                                   |
| ---------------------------------------- | ----------------------------------------- |
| `finguard_http_requests_total`           | Request count by method, path, and status |
| `finguard_http_request_duration_seconds` | Request latency histogram                 |
| `finguard_payment_requests_total`        | Payment count by status                   |
| `finguard_payment_amount_total`          | Approved payment volume                   |
| `finguard_payment_errors_total`          | API error count                           |
| `finguard_payment_store_size`            | Total persisted payments                  |

Check metrics:

```bash
curl -s http://127.0.0.1:8000/metrics | grep finguard | head -n 40
```

---

## Reliability Simulation

The service includes controlled failure and latency endpoints.

Simulate API failure:

```bash
curl -s -i http://127.0.0.1:8000/simulate/error
```

Simulate slow response:

```bash
time curl -s "http://127.0.0.1:8000/simulate/latency?delay_ms=1500" | jq
```

These endpoints will later be used to test:

* Error-budget burn
* SLO violations
* Canary rollback
* Deployment freeze decisions
* Alerting behavior

---

## Why This Service Matters

This is not a basic CRUD API.

The Payment API is the reliability signal generator for the entire FinGuard platform. It gives us real service behavior to observe, test, break, recover, and govern.

It produces the key signals needed for production-style release governance:

* API health
* Database health
* Payment success rate
* Payment failure rate
* Request latency
* Error count
* Ledger correctness
* Prometheus metrics
* Security scan readiness

This service will become the workload used in later phases for Kubernetes deployment, Prometheus monitoring, Grafana dashboards, Argo Rollouts canary releases, GitHub Actions CI/CD, and error-budget-aware deployment freezing.

