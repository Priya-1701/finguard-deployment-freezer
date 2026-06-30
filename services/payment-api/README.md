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
