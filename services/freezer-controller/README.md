The Deployment Freezer Controller is the core release-governance service in the FinGuard Deployment Freezer project.

It evaluates live Prometheus metrics and decides whether a deployment should be allowed, frozen, rolled back, or sent for manual review.

## Decisions

| Decision | Meaning |
|---|---|
| `ALLOW_DEPLOYMENT` | System is healthy enough to deploy |
| `MANUAL_REVIEW_REQUIRED` | Risk is elevated and human approval is needed |
| `FREEZE_DEPLOYMENT` | Deployment should be blocked |
| `ROLLBACK_REQUIRED` | Severe reliability issue detected; rollback is recommended |

## Signals Evaluated

- Payment API target availability
- 5xx error rate
- p95 latency
- Active critical alerts
- Active warning alerts
- Approximate error-budget burn

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check |
| GET | `/policy` | Current deployment policy |
| GET | `/decision` | Main release decision endpoint |
| GET | `/metrics` | Prometheus metrics for freezer controller |

## Run Locally

Port-forward Prometheus:

```bash
make monitoring-prometheus
