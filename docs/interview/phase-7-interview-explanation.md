In Phase 7, I added progressive delivery to the FinGuard local Kubernetes platform using Argo Rollouts.

This phase introduced controlled release strategies for the Payment API, allowing the platform to move beyond basic Kubernetes rolling updates and demonstrate safer deployment patterns such as canary and blue-green releases.

I converted the Payment API from a standard Kubernetes Deployment into an Argo Rollouts-managed workload. This allowed the release process to be controlled through a Rollout resource instead of relying only on the default Kubernetes deployment controller.

In this phase, I built and tested new Payment API Docker images such as `phase-7-v1`, `phase-7-v2`, and `phase-7-bluegreen`. Since the project runs on a local KIND cluster, I also loaded the locally built Docker images into the KIND cluster so Kubernetes could run them without pulling from a remote registry.

The Rollout resource allowed me to deploy a new version of the Payment API while keeping the stable version available. This is important because in production, new releases should not immediately replace all healthy pods. Instead, the platform should gradually expose the new version, observe its health, and only promote it when it is safe.

I also configured Kubernetes services for release traffic management, including a stable service and a preview service. The stable service represents the production traffic path, while the preview service is used to validate the new version before promotion.

This phase is important because it demonstrates how modern SRE and platform teams reduce deployment risk. Instead of pushing a new version directly to all users, the platform can validate the new version using Kubernetes health checks, Prometheus metrics, and the Deployment Freezer Controller before allowing full promotion.

The Argo Rollout can show release states such as healthy, progressing, paused, degraded, or aborted. This gives better visibility into the deployment lifecycle compared to a basic Kubernetes rollout.

In this phase, I also handled real-world Kubernetes troubleshooting scenarios such as missing Rollout resources, image pull failures, local KIND image loading, incorrect image tags, service endpoint mismatches, preview service selector issues, Kustomize overlay errors, and port-forwarding conflicts.

This phase proves that FinGuard is not just running applications on Kubernetes. It is implementing production-grade progressive delivery, where new payment service versions can be introduced safely, validated before promotion, and rolled back if reliability signals show risk.

Phase 7 strengthens the project by connecting deployment strategy with release safety. It shows how a fintech payment platform can reduce blast radius, validate new releases gradually, and avoid exposing all users to a potentially risky version.

