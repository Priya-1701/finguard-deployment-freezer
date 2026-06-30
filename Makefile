.PHONY: phase0-check tree docker-check kind-smoke-test kind-smoke-delete git-status \
        payment-api-install payment-api-test payment-api-run payment-api-health payment-api-metrics \
        payment-api-docker-build payment-api-docker-run payment-api-docker-logs payment-api-docker-stop \
        payment-api-docker-health payment-api-docker-metrics payment-api-compose-up payment-api-compose-down \
        payment-api-compose-reset payment-api-compose-logs payment-api-db-health payment-api-db-shell \
        payment-api-trivy-scan kind-create kind-delete kind-load-images k8s-apply k8s-delete \
        k8s-status k8s-wait k8s-logs k8s-port-forward k8s-db-shell k8s-restart k8s-scale-up k8s-scale-down

phase0-check:
	./scripts/phase0_doctor.sh

tree:
	tree -L 4

docker-check:
	docker --version
	docker info
	docker run hello-world

kind-smoke-test:
	kind create cluster --name finguard-phase0-test
	kubectl cluster-info --context kind-finguard-phase0-test
	kubectl get nodes
	kubectl get pods -A

kind-smoke-delete:
	kind delete cluster --name finguard-phase0-test

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

payment-api-docker-build:
	cd services/payment-api && docker compose build

payment-api-docker-run:
	cd services/payment-api && docker compose up -d

payment-api-docker-logs:
	cd services/payment-api && docker compose logs payment-api

payment-api-docker-health:
	curl -s http://127.0.0.1:8000/health | jq

payment-api-docker-metrics:
	curl -s http://127.0.0.1:8000/metrics | grep finguard | head -n 30

payment-api-docker-stop:
	cd services/payment-api && docker compose down

payment-api-compose-up:
	cd services/payment-api && docker compose up --build -d

payment-api-compose-down:
	cd services/payment-api && docker compose down

payment-api-compose-reset:
	cd services/payment-api && docker compose down --volumes --remove-orphans

payment-api-compose-logs:
	cd services/payment-api && docker compose logs

payment-api-db-shell:
	docker exec -it finguard-postgres psql -U finguard_user -d finguard

payment-api-trivy-scan:
	trivy image --severity HIGH,CRITICAL --ignore-unfixed finguard/payment-api:phase-3

kind-create:
	kind create cluster --name finguard-local --config platform/kind/finguard-kind-config.yaml

kind-delete:
	kind delete cluster --name finguard-local

kind-load-images:
	docker build -t finguard/payment-api:phase-4 services/payment-api
	docker pull postgres:16-alpine
	kind load docker-image finguard/payment-api:phase-4 --name finguard-local
	kind load docker-image postgres:16-alpine --name finguard-local

k8s-apply:
	kubectl apply -k platform/k8s/overlays/local

k8s-delete:
	kubectl delete -k platform/k8s/overlays/local

k8s-status:
	kubectl -n finguard get all
	kubectl -n finguard get pvc
	kubectl -n finguard get svc

k8s-wait:
	kubectl -n finguard wait --for=condition=ready pod/postgres-0 --timeout=180s
	kubectl -n finguard rollout status deployment/payment-api --timeout=180s

k8s-logs:
	kubectl -n finguard logs postgres-0 --tail=50
	kubectl -n finguard logs deployment/payment-api --tail=50

k8s-port-forward:
	kubectl -n finguard port-forward svc/payment-api 8000:8000

k8s-db-shell:
	kubectl -n finguard exec -it postgres-0 -- psql -U finguard_user -d finguard

k8s-restart:
	kubectl -n finguard rollout restart deployment/payment-api
	kubectl -n finguard rollout status deployment/payment-api --timeout=180s

k8s-scale-up:
	kubectl -n finguard scale deployment/payment-api --replicas=2
	kubectl -n finguard rollout status deployment/payment-api --timeout=180s

k8s-scale-down:
	kubectl -n finguard scale deployment/payment-api --replicas=1
	kubectl -n finguard rollout status deployment/payment-api --timeout=180s
