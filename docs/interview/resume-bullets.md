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
