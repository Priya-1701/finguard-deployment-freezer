# Phase 1 Interview Explanation

In Phase 1, I built the first microservice for FinGuard Deployment Freezer: a Python FastAPI-based Payment API.

The service simulates a fintech payment authorization system with endpoints for health checks, readiness checks, payment creation, payment lookup, simulated failures, simulated latency, and Prometheus metrics.

I intentionally used an in-memory payment store in this phase to keep the first service lightweight and testable before introducing PostgreSQL in a later phase.

The key production/SRE idea in this phase is that the service is designed to emit reliability signals from the beginning. It exposes request counts, request duration, payment status counts, payment errors, and payment store size. These signals will later support SLO calculation, error-budget monitoring, deployment freeze decisions, canary validation, and rollback automation.

I also added pytest-based API tests so the service can be validated automatically before Dockerization, Kubernetes deployment, and CI/CD integration.
