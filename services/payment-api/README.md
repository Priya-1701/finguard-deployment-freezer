# Payment API

The Payment API is the first microservice in the FinGuard Deployment Freezer project.

It simulates a fintech payment authorization service and exposes endpoints for:

- Health checks
- Readiness checks
- Payment creation
- Payment lookup
- Failure simulation
- Latency simulation
- Prometheus metrics

## Why this service exists

FinGuard Deployment Freezer needs a realistic service that can produce reliability signals.

This API gives us:

- Successful payment traffic
- Declined payment traffic
- Simulated failures
- Simulated latency
- Prometheus metrics
- Testable API behavior

These signals will later be used by the deployment freezer controller to decide whether a release should continue, pause, rollback, or freeze.

## Phase 2: Dockerized Payment API

Phase 2 packages the Payment API into a Docker image.

## Build Docker Image

From project root:

```bash
cd services/payment-api
docker build -t finguard/payment-api:phase-2 .

## Phase 3: PostgreSQL and Ledger Persistence

Phase 3 replaces the temporary in-memory payment store with database-backed persistence.

The Payment API now stores:

- Payment transactions
- Ledger entries

## Database Tables

### `payment_transactions`

Stores the payment decision.

Important columns:

- `payment_id`
- `status`
- `amount`
- `currency`
- `merchant_id`
- `customer_id`
- `idempotency_key`
- `message`
- `created_at`

### `ledger_entries`

Stores money movement records for approved payments.

Approved payments create two ledger entries:

- `DEBIT_CUSTOMER`
- `CREDIT_MERCHANT`

Declined payments do not create ledger entries.

## Run API with PostgreSQL

From project root:

```bash
make payment-api-compose-up
