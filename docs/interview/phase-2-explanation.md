# Phase 2 Interview Explanation

In Phase 2, I containerized the Python FastAPI Payment API using Docker.

I created a Dockerfile using a slim Python base image, installed only the required dependencies, copied the application code, exposed port 8000, added a Docker healthcheck, and configured the service to run through Uvicorn.

I also configured the container to run as a non-root user named `finguard`, which is a basic production container security practice.

I added a `.dockerignore` file to avoid copying unnecessary files such as local virtual environments, cache files, secrets, Git metadata, and tests into the runtime image.

After building the image, I validated the container by testing the `/health`, `/ready`, `/pay`, `/simulate/error`, `/simulate/latency`, and `/metrics` endpoints from the host machine.

I also added Docker Compose support to make local container execution repeatable, and I scanned the image using Trivy for high and critical vulnerabilities.

This phase proves that the Payment API can now run consistently as a container, which prepares it for Kubernetes deployment in the next phases.
