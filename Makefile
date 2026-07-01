.PHONY: phase0-check tree docker-check git-status \
        payment-api-install payment-api-test payment-api-run payment-api-health payment-api-db-health payment-api-metrics \
        payment-api-compose-up payment-api-compose-down payment-api-compose-reset payment-api-compose-logs payment-api-db-shell \
        payment-api-trivy-scan \
        kind-create kind-delete kind-load-images k8s-apply k8s-delete k8s-status k8s-wait k8s-port-forward

phase0-check:
	./scripts/phase0_doctor.sh

tree:
	tree -L 4

docker-check:
	docker --version
	docker info
	docker run hello-world

git-status:
	git status

payment-api-install:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && python -m pip install -r services/payment-api/requirements.txt

payment-api-test:
	. .venv/bin/activate && pytest

payment-api-run:
	cd services/payment-api && ../../.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

payment-api-health:
	curl -s http://127.0.0.1:8000/health | jq

payment-api-db-health:
	curl -s http://127.0.0.1:8000/db/health | jq

payment-api-metrics:
	curl -s http://127.0.0.1:8000/metrics | grep finguard | head -n 30

payment-api-compose-up:
	cd services/payment-api && docker compose up --build -d

payment-api-compose-down:
	cd services/payment-api && docker compose down

payment-api-compose-reset:
	cd services/payment-api && docker compose down --volumes --remove-orphans

payment-api-compose-logs:
	cd services/payment-api && docker compose logs

payment-api-db-shell:
	cd services/payment-api && docker compose exec postgres psql -U finguard_user -d finguard

payment-api-trivy-scan:
	trivy image --severity HIGH,CRITICAL --ignore-unfixed finguard/payment-api:phase-4

kind-create:
	kind create cluster --name finguard-local --config platform/kind/finguard-kind-config.yaml

kind-delete:
	kind delete cluster --name finguard-local

kind-load-images:
	if [ "$$(uname -m)" = "arm64" ]; then \
		DOCKER_PLATFORM="linux/arm64"; \
	else \
		DOCKER_PLATFORM="linux/amd64"; \
	fi; \
	docker buildx build \
		--platform "$$DOCKER_PLATFORM" \
		--provenance=false \
		--sbom=false \
		--load \
		-t finguard/payment-api:phase-4 \
		services/payment-api
	docker save finguard/payment-api:phase-4 -o /tmp/finguard-payment-api-phase-4.tar
	kind load image-archive /tmp/finguard-payment-api-phase-4.tar --name finguard-local
	docker exec finguard-local-control-plane crictl images | grep finguard

k8s-apply:
	kubectl apply -k platform/k8s/overlays/local

k8s-delete:
	kubectl delete -k platform/k8s/overlays/local || true

k8s-status:
	kubectl get all -n finguard

k8s-wait:
	kubectl -n finguard wait --for=condition=ready pod/finguard-postgres-0 --timeout=180s
	kubectl -n finguard rollout status deployment/payment-api --timeout=180s

k8s-port-forward:
	kubectl port-forward -n finguard svc/payment-api 8000:8000

.PHONY: monitoring-install monitoring-status monitoring-apply-dashboard monitoring-prometheus monitoring-grafana monitoring-alertmanager monitoring-uninstall monitoring-test-traffic monitoring-test-errors monitoring-test-latency

monitoring-install:
	kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update
	helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
		--namespace monitoring \
		--values observability/prometheus/kube-prometheus-stack-values.yaml

monitoring-status:
	kubectl -n monitoring get pods
	kubectl -n monitoring get svc
	kubectl -n finguard get servicemonitor
	kubectl -n finguard get prometheusrule

monitoring-apply-dashboard:
	kubectl apply -f observability/grafana/dashboards/payment-api-dashboard-configmap.yaml

monitoring-prometheus:
	kubectl -n monitoring port-forward svc/monitoring-prometheus 9090:9090

monitoring-grafana:
	kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80

monitoring-alertmanager:
	kubectl -n monitoring port-forward svc/monitoring-alertmanager 9093:9093

monitoring-uninstall:
	helm uninstall monitoring -n monitoring || true
	kubectl delete namespace monitoring || true

monitoring-test-traffic:
	for i in $$(seq 1 20); do \
		curl -s -X POST http://127.0.0.1:8000/pay \
			-H "Content-Type: application/json" \
			-d "{\"amount\": $$((100 + i)), \"currency\": \"INR\", \"merchant_id\": \"merchant_obs_001\", \"customer_id\": \"customer_obs_$$i\", \"idempotency_key\": \"obs-order-$$i\"}" >/dev/null; \
	done

monitoring-test-errors:
	for i in $$(seq 1 20); do \
		curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/simulate/error; \
		sleep 1; \
	done

monitoring-test-latency:
	for i in $$(seq 1 10); do \
		curl -s "http://127.0.0.1:8000/simulate/latency?delay_ms=1200" >/dev/null; \
		sleep 1; \
	done

.PHONY: freezer-test freezer-build freezer-load freezer-apply freezer-status freezer-port-forward freezer-decision freezer-policy freezer-metrics freezer-logs

freezer-test:
	. .venv/bin/activate && pytest services/freezer-controller/tests

freezer-build:
	docker build -t finguard/freezer-controller:phase-6 services/freezer-controller

freezer-load:
	kind load docker-image finguard/freezer-controller:phase-6 --name finguard-local

freezer-apply:
	kubectl apply -k platform/k8s/overlays/local

freezer-status:
	kubectl -n finguard rollout status deployment/freezer-controller --timeout=180s
	kubectl -n finguard get pods
	kubectl -n finguard get svc freezer-controller

freezer-port-forward:
	kubectl -n finguard port-forward svc/freezer-controller 8010:8010

freezer-decision:
	curl -s http://127.0.0.1:8010/decision | jq

freezer-policy:
	curl -s http://127.0.0.1:8010/policy | jq

freezer-metrics:
	curl -s http://127.0.0.1:8010/metrics | grep finguard_freezer

freezer-logs:
	kubectl -n finguard logs deployment/freezer-controller --tail=100

.PHONY: rollouts-install rollouts-status rollouts-dashboard rollout-get rollout-watch rollout-promote rollout-abort rollout-undo rollout-canary-apply rollout-bluegreen-apply rollout-delete-deployment

rollouts-install:
	kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
	kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=180s

rollouts-status:
	kubectl -n argo-rollouts get pods
	kubectl -n finguard get rollout
	kubectl -n finguard get analysisrun || true

rollouts-dashboard:
	kubectl argo rollouts dashboard

rollout-get:
	kubectl argo rollouts get rollout payment-api -n finguard

rollout-watch:
	kubectl argo rollouts get rollout payment-api -n finguard --watch

rollout-promote:
	kubectl argo rollouts promote payment-api -n finguard

rollout-abort:
	kubectl argo rollouts abort payment-api -n finguard

rollout-undo:
	kubectl argo rollouts undo payment-api -n finguard

rollout-delete-deployment:
	kubectl -n finguard delete deployment payment-api --ignore-not-found=true

rollout-canary-apply:
	kubectl -n finguard delete deployment payment-api --ignore-not-found=true
	kubectl apply -k platform/k8s/overlays/local

rollout-bluegreen-apply:
	kubectl -n finguard delete rollout payment-api --ignore-not-found=true
	kubectl apply -k platform/k8s/overlays/bluegreen

.PHONY: rollouts-install rollouts-status rollouts-dashboard rollout-get rollout-watch rollout-promote rollout-abort rollout-undo rollout-canary-apply rollout-bluegreen-apply rollout-delete-deployment

rollouts-install:
	kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
	kubectl -n argo-rollouts rollout status deployment/argo-rollouts --timeout=180s

rollouts-status:
	kubectl -n argo-rollouts get pods
	kubectl -n finguard get rollout
	kubectl -n finguard get analysisrun || true

rollouts-dashboard:
	kubectl argo rollouts dashboard

rollout-get:
	kubectl argo rollouts get rollout payment-api -n finguard

rollout-watch:
	kubectl argo rollouts get rollout payment-api -n finguard --watch

rollout-promote:
	kubectl argo rollouts promote payment-api -n finguard

rollout-abort:
	kubectl argo rollouts abort payment-api -n finguard

rollout-undo:
	kubectl argo rollouts undo payment-api -n finguard

rollout-delete-deployment:
	kubectl -n finguard delete deployment payment-api --ignore-not-found=true

rollout-canary-apply:
	kubectl -n finguard delete deployment payment-api --ignore-not-found=true
	kubectl apply -k platform/k8s/overlays/local

rollout-bluegreen-apply:
	kubectl -n finguard delete rollout payment-api --ignore-not-found=true
	kubectl apply -k platform/k8s/overlays/bluegreen
