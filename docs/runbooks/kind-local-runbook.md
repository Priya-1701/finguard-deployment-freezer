# KIND Local Kubernetes Runbook

## Purpose

This runbook explains how to deploy and validate FinGuard Payment API and PostgreSQL on a local KIND Kubernetes cluster.

## Create Cluster

```bash
kind create cluster --name finguard-local --config platform/kind/finguard-kind-config.yaml
