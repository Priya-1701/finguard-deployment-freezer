#!/usr/bin/env bash

set -euo pipefail

echo "=============================================="
echo " FinGuard Deployment Freezer - Phase 0 Doctor "
echo "=============================================="
echo

missing_tools=()

check_tool() {
  local tool_name="$1"

  if command -v "$tool_name" >/dev/null 2>&1; then
    echo "✅ $tool_name found: $(command -v "$tool_name")"
  else
    echo "❌ $tool_name missing"
    missing_tools+=("$tool_name")
  fi
}

echo "Checking required CLI tools..."
check_tool git
check_tool gh
check_tool python3
check_tool pip3
check_tool docker
check_tool kubectl
check_tool kind
check_tool helm
check_tool trivy
check_tool k6
check_tool jq
check_tool tree

echo
echo "Checking versions..."
git --version || true
python3 --version || true
docker --version || true
kubectl version --client || true
kind version || true
helm version || true
trivy --version | head -n 1 || true
k6 version || true
jq --version || true

echo
echo "Checking Docker daemon..."
if docker info >/dev/null 2>&1; then
  echo "✅ Docker daemon is running"
else
  echo "❌ Docker daemon is not running"
  echo "Open Docker Desktop and wait until it says Docker is running."
  exit 1
fi

echo
echo "Checking project folders..."
required_dirs=(
  "services/payment-api/app"
  "services/freezer-controller/app"
  "services/ledger-worker/app"
  "platform/kind"
  "platform/k8s/base"
  "platform/k8s/overlays/local"
  "platform/argocd"
  "platform/argo-rollouts"
  "platform/helm-values"
  "observability/prometheus"
  "observability/grafana/dashboards"
  "observability/grafana/provisioning"
  "observability/alertmanager"
  "load-tests/k6"
  "scripts"
  "docs/architecture"
  "docs/screenshots/phase-0"
  "docs/runbooks"
  "docs/interview"
  "infra/aws-eks/terraform"
  ".github/workflows"
)

for dir in "${required_dirs[@]}"; do
  if [[ -d "$dir" ]]; then
    echo "✅ $dir"
  else
    echo "❌ Missing directory: $dir"
    exit 1
  fi
done

echo
if [[ ${#missing_tools[@]} -gt 0 ]]; then
  echo "Missing tools:"
  printf ' - %s\n' "${missing_tools[@]}"
  exit 1
fi

echo "=============================================="
echo " ✅ Phase 0 workstation check passed"
echo "=============================================="
