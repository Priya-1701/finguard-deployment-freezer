# Phase 5 Interview Explanation

In Phase 5, I added observability to the FinGuard local Kubernetes platform using kube-prometheus-stack.

This installed Prometheus, Grafana, Alertmanager, Prometheus Operator, kube-state-metrics, and node-exporter into a dedicated `monitoring` namespace.

I created a ServiceMonitor for the Payment API so Prometheus can automatically scrape the `/metrics` endpoint exposed by the FastAPI service. I also created PrometheusRule alerts for Payment API target availability, high error rate, high p95 latency, and increasing payment errors.

I added a custom Grafana dashboard for the Payment API showing target health, request rate, 5xx error rate, p95 latency, payment status trends, error types, approved payment volume, and persisted payment count.

This phase is important because deployment governance requires real observability signals. A production-grade release controller should not approve deployments based only on CI success. It should also consider live service health, error rate, latency, and alert state.

This observability foundation prepares the project for the next phase, where the Deployment Freezer Controller will evaluate metrics and decide whether a release should continue, pause, rollback, or freeze.
