# Resume Bullets

- Designed the foundation for a production-style fintech release governance platform using Python, Docker, Kubernetes, GitHub Actions, Argo CD, Argo Rollouts, Prometheus, Grafana, k6, and Trivy.

- Built a local-first DevOps/SRE project structure with service, platform, observability, load-testing, CI/CD, GitOps, and Terraform layers to support progressive delivery and error-budget-aware release controls.

- Automated workstation validation using shell scripts and Makefile targets to verify Docker, KIND, kubectl, Helm, Python, k6, and Trivy readiness before application deployment.

- Established a budget-safe cloud migration path by starting with local KIND Kubernetes and deferring AWS EKS provisioning to a later Terraform-controlled phase with explicit cleanup and cost-control steps.

## Phase 1 Resume Bullets

- Built a Python FastAPI payment microservice with health, readiness, payment authorization, failure simulation, latency simulation, and Prometheus metrics endpoints.

- Implemented API validation and automated pytest coverage for core payment flows, declined transactions, simulated failures, latency checks, and metrics exposure.

- Designed service-level reliability signals including request count, request duration, payment status, error count, and payment store size to support future SLO and error-budget automation.

- Created local runbooks and documentation for operating, testing, and troubleshooting the payment API from macOS Terminal.

## Phase 2 Resume Bullets

- Containerized a Python FastAPI fintech payment service using Docker with a slim Python runtime, non-root user, exposed service port, and Docker healthcheck.

- Implemented `.dockerignore` and Docker layer caching practices to reduce build context size and avoid packaging secrets, virtual environments, and unnecessary local files.

- Validated containerized API behavior through Docker run and Docker Compose workflows, including health checks, payment creation, latency simulation, failure simulation, and Prometheus metrics exposure.

- Integrated Trivy image scanning into the local workflow to identify high and critical container vulnerabilities before CI/CD and Kubernetes deployment.

## Phase 3 Resume Bullets

- Integrated PostgreSQL persistence into a Python FastAPI payment service using SQLAlchemy ORM and Docker Compose.

- Designed fintech-style `payment_transactions` and `ledger_entries` tables to persist payment decisions and accounting movement records.

- Implemented ledger generation logic where approved payments create debit and credit ledger entries while declined payments are persisted without financial movement.

- Added database health checking through a `/db/health` endpoint to support future Kubernetes readiness, observability, alerting, and deployment-freezer decisions.

- Built a local Docker Compose stack for Payment API and PostgreSQL, including database health checks, persistent volumes, and direct SQL verification through psql.

## Phase 4 Resume Bullets

- Deployed a containerized FastAPI payment service and PostgreSQL database onto a local KIND Kubernetes cluster using production-style Kubernetes manifests.

- Implemented Kubernetes Namespace, ConfigMap, Secret, Service, StatefulSet, Deployment, PersistentVolumeClaim, probes, and resource requests/limits.

- Configured PostgreSQL as a StatefulSet with persistent storage and deployed the Payment API as a stateless Kubernetes Deployment.

- Added startup, liveness, and readiness probes, including database-aware readiness checks to prevent routing traffic to unhealthy application pods.

- Validated Kubernetes service behavior using kubectl port-forward, API health checks, database health checks, payment creation, ledger verification, and direct PostgreSQL inspection.
