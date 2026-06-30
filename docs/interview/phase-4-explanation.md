# Phase 4 Interview Explanation

In Phase 4, I moved the FinGuard Payment API and PostgreSQL stack from Docker Compose into a local Kubernetes cluster using KIND.

I created Kubernetes manifests for namespace isolation, ConfigMap-based configuration, Secret-based local credentials, PostgreSQL networking, PostgreSQL StatefulSet storage, Payment API Deployment, and Payment API Service.

PostgreSQL was deployed as a StatefulSet because it needs stable identity and persistent storage. The Payment API was deployed as a Deployment because it is stateless and can be restarted, scaled, and rolled out safely.

I added Kubernetes health probes to make the workload more production-like. The Payment API uses a startup probe and liveness probe on `/health`, and a readiness probe on `/db/health` so Kubernetes only routes traffic to the API when its database dependency is healthy.

I also added CPU and memory requests and limits to both PostgreSQL and Payment API. This improves scheduling behavior and makes the manifests closer to production Kubernetes standards.

This phase proves that the application is now Kubernetes-ready and prepares the platform for Prometheus monitoring, Grafana dashboards, Argo Rollouts, GitOps, and AWS EKS deployment.
