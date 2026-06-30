# FinGuard Deployment Freezer

## Error-Budget-Aware Release Governance Platform for FinTech Payments

FinGuard Deployment Freezer is a production-style DevOps/SRE platform that simulates how a fintech payment system can make safer release decisions using service health, database health, SLO signals, error-budget burn, observability, security scans, and progressive delivery controls.

Most CI/CD pipelines answer:

> Did the build pass?

FinGuard answers a stronger production question:

> Is the platform reliable enough right now to safely deploy?

This project is designed to demonstrate real-world release governance practices used in high-scale engineering environments where deployment safety, customer trust, observability, rollback speed, and operational discipline matter.

---

## Project Vision

In fintech systems, every failed payment, delayed transaction, database issue, or unstable release can directly affect:

* Customers
* Merchants
* Reconciliation
* Support teams
* Compliance workflows
* Business trust

FinGuard Deployment Freezer is built around one core idea:

> Deployment should not be controlled only by pipeline success. It should also be controlled by live reliability signals.

The platform will eventually decide whether a release should be:

* Approved
* Paused
* Rolled back
* Frozen

based on production-style indicators such as:

* API health
* Database health
* Error rate
* Latency
* Payment failure rate
* Error-budget burn
* Active alerts
* Canary health
* Security scan results
* Progressive delivery analysis

---

## Current Status

| Phase    | Status    | Description                                                                              |
| -------- | --------- | ---------------------------------------------------------------------------------------- |
| Phase 0  | Completed | macOS Terminal setup, tools, project structure, GitHub foundation                        |
| Phase 1  | Completed | FastAPI Payment API with health, readiness, metrics, failure simulation, and tests       |
| Phase 2  | Completed | Dockerized Payment API with Dockerfile, Docker Compose, healthcheck, and Trivy workflow  |
| Phase 3  | Completed | PostgreSQL persistence, payment transactions, ledger entries, and database health checks |
| Phase 4  | Completed  | Local KIND Kubernetes deployment                                                         |
| Phase 5  | Upcoming  | Prometheus and Grafana observability                                                     |
| Phase 6  | Upcoming  | Error-budget-aware deployment freezer controller                                         |
| Phase 7  | Upcoming  | Argo Rollouts canary, blue-green, promotion, and rollback                                |
| Phase 8  | Upcoming  | GitHub Actions CI/CD pipeline                                                            |
| Phase 9  | Upcoming  | Argo CD GitOps                                                                           |
| Phase 10 | Upcoming  | AWS EKS and ECR using Terraform                                                          |
| Phase 11 | Upcoming  | Final documentation, screenshots, dashboards, demo, resume, and interview polish         |

---

## What Has Been Built So Far

The project currently includes a working fintech-style Payment API with:

* Python FastAPI service
* Dockerized runtime
* Docker Compose local environment
* PostgreSQL-backed persistence
* Payment transaction storage
* Ledger entry creation
* API health endpoint
* API readiness endpoint
* Database health endpoint
* Prometheus metrics endpoint
* Failure simulation endpoint
* Latency simulation endpoint
* Pytest test coverage
* Trivy image scanning workflow
* Makefile automation
* Runbooks and interview documentation

---

## High-Level Architecture

```text
Developer
   |
   | git commit / git push
   v
GitHub Repository
   |
   | future CI/CD pipeline
   v
GitHub Actions
   |
   | test, build, scan, validate
   v
Docker Image
   |
   | local first
   v
Docker Compose / KIND Kubernetes
   |
   v
Payment API
   |
   | persists transactions and ledger records
   v
PostgreSQL
   |
   | exposes reliability signals
   v
Prometheus Metrics
   |
   v
Grafana Dashboards
   |
   v
Deployment Freezer Controller
   |
   | allow / pause / rollback / freeze
   v
Argo Rollouts + Argo CD
```

---

## Core Tech Stack

| Area                        | Technology     |
| --------------------------- | -------------- |
| Programming Language        | Python         |
| API Framework               | FastAPI        |
| Database                    | PostgreSQL     |
| ORM                         | SQLAlchemy     |
| Containerization            | Docker         |
| Local Multi-Service Runtime | Docker Compose |
| Local Kubernetes            | KIND           |
| Kubernetes CLI              | kubectl        |
| Kubernetes Package Manager  | Helm           |
| CI/CD                       | GitHub Actions |
| GitOps                      | Argo CD        |
| Progressive Delivery        | Argo Rollouts  |
| Monitoring                  | Prometheus     |
| Dashboarding                | Grafana        |
| Alerting                    | Alertmanager   |
| Load Testing                | k6             |
| Security Scanning           | Trivy          |
| Cloud Platform              | AWS            |
| Cloud Kubernetes            | AWS EKS        |
| Container Registry          | AWS ECR        |
| Infrastructure as Code      | Terraform      |
| Version Control             | Git + GitHub   |

---

## Repository Structure

```text
finguard-deployment-freezer/
├── .github/
│   └── workflows/
├── docs/
│   ├── architecture/
│   ├── interview/
│   ├── runbooks/
│   └── screenshots/
├── infra/
│   └── aws-eks/
│       └── terraform/
├── load-tests/
│   └── k6/
├── observability/
│   ├── alertmanager/
│   ├── grafana/
│   └── prometheus/
├── platform/
│   ├── argocd/
│   ├── argo-rollouts/
│   ├── helm-values/
│   ├── kind/
│   └── k8s/
├── scripts/
├── services/
│   ├── freezer-controller/
│   ├── ledger-worker/
│   └── payment-api/
├── .env.example
├── .gitignore
├── Makefile
├── pytest.ini
└── README.md
```

---

## Payment API

The Payment API is the first implemented service in the platform.

It simulates a fintech payment authorization system and generates the signals that will later drive release-governance decisions.

### Payment API Capabilities

| Capability             | Status      |
| ---------------------- | ----------- |
| Health check           | Implemented |
| Readiness check        | Implemented |
| Database health check  | Implemented |
| Payment creation       | Implemented |
| Payment lookup         | Implemented |
| Ledger lookup          | Implemented |
| PostgreSQL persistence | Implemented |
| Prometheus metrics     | Implemented |
| Failure simulation     | Implemented |
| Latency simulation     | Implemented |
| Docker runtime         | Implemented |
| Docker Compose stack   | Implemented |
| Trivy scan workflow    | Implemented |
| Pytest coverage        | Implemented |

### Payment API Endpoints

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
| GET    | `/simulate/latency?delay_ms=1000` | Simulate slow API response        |
| GET    | `/metrics`                        | Prometheus metrics endpoint       |

---

## Database Design

The Payment API currently uses PostgreSQL with two core tables.

### `payment_transactions`

Stores final payment decisions.

| Field             | Purpose                                  |
| ----------------- | ---------------------------------------- |
| `payment_id`      | Unique payment identifier                |
| `status`          | Payment status: `APPROVED` or `DECLINED` |
| `amount`          | Payment amount                           |
| `currency`        | Payment currency                         |
| `merchant_id`     | Merchant receiving payment               |
| `customer_id`     | Customer making payment                  |
| `idempotency_key` | Duplicate request protection reference   |
| `message`         | Payment decision message                 |
| `created_at`      | Transaction timestamp                    |

### `ledger_entries`

Stores accounting-style money movement records.

For every approved payment, the service creates:

```text
DEBIT_CUSTOMER
CREDIT_MERCHANT
```

Declined payments are stored in `payment_transactions`, but no ledger entries are created.

This makes the service more realistic than a basic CRUD API because payment decisions and financial movement records are modeled separately.

---

## Reliability Signals

The service is intentionally designed to emit operational signals from the beginning.

| Signal                  | Why It Matters                                     |
| ----------------------- | -------------------------------------------------- |
| API health              | Confirms the service process is alive              |
| Readiness               | Confirms the service is ready to receive traffic   |
| Database health         | Confirms critical dependency connectivity          |
| Error count             | Helps detect bad releases or incidents             |
| Request latency         | Supports p95 latency SLOs                          |
| Payment success/failure | Supports business-level reliability analysis       |
| Ledger records          | Supports transaction correctness checks            |
| Prometheus metrics      | Enables dashboards, alerts, and error-budget logic |

---

## Prometheus Metrics

The Payment API exposes metrics at:

```text
/metrics
```

Important metrics include:

| Metric                                   | Purpose                                         |
| ---------------------------------------- | ----------------------------------------------- |
| `finguard_http_requests_total`           | Total HTTP requests by method, path, and status |
| `finguard_http_request_duration_seconds` | HTTP request latency histogram                  |
| `finguard_payment_requests_total`        | Payment count by payment status                 |
| `finguard_payment_amount_total`          | Approved payment volume by currency             |
| `finguard_payment_errors_total`          | Error count by error type                       |
| `finguard_payment_store_size`            | Total persisted payment count                   |

---

## Run Locally

### Start Payment API with PostgreSQL

```bash
cd ~/Projects/finguard-deployment-freezer
make payment-api-compose-up
```

### Check API Health

```bash
make payment-api-health
```

### Check Database Health

```bash
make payment-api-db-health
```

### Stop the Stack

```bash
make payment-api-compose-down
```

### Reset Database

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

Expected response shape:

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

Open the PostgreSQL shell:

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

## Reliability Simulation

The Payment API includes controlled failure and latency endpoints.

### Simulate API Failure

```bash
curl -s -i http://127.0.0.1:8000/simulate/error
```

### Simulate Slow Response

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

## Makefile Commands

| Command                          | Purpose                                 |
| -------------------------------- | --------------------------------------- |
| `make payment-api-test`          | Run Payment API tests                   |
| `make payment-api-compose-up`    | Start Payment API and PostgreSQL        |
| `make payment-api-compose-down`  | Stop Docker Compose stack               |
| `make payment-api-compose-reset` | Stop stack and delete PostgreSQL volume |
| `make payment-api-health`        | Check API health                        |
| `make payment-api-db-health`     | Check database health                   |
| `make payment-api-db-shell`      | Open PostgreSQL shell                   |
| `make payment-api-docker-build`  | Build Docker image                      |
| `make payment-api-trivy-scan`    | Scan Docker image with Trivy            |

---

## Design Principles

This project is built using production-oriented engineering principles:

### Local First

The platform starts locally with Docker Compose and KIND before moving to AWS EKS.

### Reliability First

The system is designed around SLOs, SLIs, error budgets, health checks, and measurable operational signals.

### Security Aware

Container scanning with Trivy is introduced early and will later become part of CI/CD.

### Observable by Design

Metrics are exposed from the first service so monitoring and dashboards can be added naturally.

### Progressive Delivery Ready

The workload is being prepared for canary, blue-green, rolling deployment, promotion, and rollback strategies.

### Cloud Ready

The repository already contains a future path for AWS EKS, ECR, IAM, VPC, and Terraform.

---

## Why This Project Stands Out

This is not a generic CI/CD or Kubernetes demo.

FinGuard Deployment Freezer combines multiple real-world platform engineering and SRE concepts:

* Fintech-style payment workload
* Persistent transaction storage
* Ledger-style financial records
* API and database health checks
* Prometheus-ready metrics
* Failure and latency simulation
* Dockerized microservice architecture
* Security scanning workflow
* Future Kubernetes deployment
* Future progressive delivery
* Future GitOps
* Future AWS EKS deployment
* Future error-budget-aware release governance

The goal is to show not just how to deploy software, but how to decide whether software should be deployed at all.

---

## Future Roadmap

### Phase 4 — Local Kubernetes with KIND

Planned work:

* Kubernetes namespace
* ConfigMap
* Secret
* PostgreSQL workload
* Payment API Deployment
* Payment API Service
* Liveness probe
* Readiness probe
* Resource requests and limits
* Local image loading into KIND

### Phase 5 — Observability

Planned work:

* Prometheus installation
* Grafana installation
* Payment API dashboard
* PostgreSQL dashboard
* Error rate panels
* Latency panels
* Payment success/failure panels

### Phase 6 — Deployment Freezer Controller

Planned work:

* Error-budget evaluation logic
* Deployment allow/freeze API
* Prometheus query integration
* Alert-aware deployment decision
* Release governance policy

### Phase 7 — Progressive Delivery

Planned work:

* Argo Rollouts
* Canary strategy
* Blue-green strategy
* Automated rollback
* Promotion gates

### Phase 8 — CI/CD

Planned work:

* GitHub Actions pipeline
* Test stage
* Docker build stage
* Trivy scan stage
* Deployment-freezer check stage

### Phase 9 — GitOps

Planned work:

* Argo CD application
* Git-based Kubernetes sync
* Drift detection
* GitOps promotion flow

### Phase 10 — AWS EKS

Planned work:

* Terraform VPC
* EKS cluster
* ECR repository
* IAM roles
* Node group
* Budget-safe cleanup workflow

---

## Budget-Safe AWS Approach

The project starts locally to avoid unnecessary cloud cost.

AWS EKS will be introduced only after the local platform is complete. The AWS phase will include:

* Small node groups
* Explicit cleanup commands
* Terraform destroy workflow
* ECR image cleanup
* Budget alert guidance
* No unnecessary long-running resources

---

## Documentation

| Location                         | Purpose                                   |
| -------------------------------- | ----------------------------------------- |
| `services/payment-api/README.md` | Payment API documentation                 |
| `docs/runbooks/`                 | Operational runbooks                      |
| `docs/interview/`                | Interview explanations and resume bullets |
| `docs/architecture/`             | Architecture notes and diagrams           |
| `docs/screenshots/`              | Final proof screenshots                   |

Screenshots will be collected and pushed during the final documentation phase.

---

## Current Engineering Outcome

At the current stage, FinGuard has a working containerized fintech payment service with PostgreSQL persistence and reliability instrumentation.

The foundation is now ready for:

```text
Docker Compose → KIND Kubernetes → Prometheus/Grafana → Argo Rollouts → GitHub Actions → Argo CD → AWS EKS
```

This project is being built as a complete DevOps/SRE portfolio project focused on production reliability, release safety, and cloud-native platform engineering.

