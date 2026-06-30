.PHONY: phase0-check tree docker-check kind-smoke-test kind-smoke-delete git-status \
        payment-api-install payment-api-test payment-api-run payment-api-health payment-api-metrics \
        payment-api-docker-build payment-api-docker-run payment-api-docker-logs payment-api-docker-stop \
        payment-api-docker-health payment-api-docker-metrics payment-api-compose-up payment-api-compose-down \
        payment-api-trivy-scan

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

payment-api-metrics:
	curl -s http://127.0.0.1:8000/metrics | grep finguard | head -n 30

payment-api-docker-build:
	cd services/payment-api && docker build -t finguard/payment-api:phase-2 .

payment-api-docker-run:
	docker run -d --name finguard-payment-api -p 8000:8000 finguard/payment-api:phase-2

payment-api-docker-logs:
	docker logs finguard-payment-api

payment-api-docker-health:
	curl -s http://127.0.0.1:8000/health | jq

payment-api-docker-metrics:
	curl -s http://127.0.0.1:8000/metrics | grep finguard | head -n 30

payment-api-docker-stop:
	docker stop finguard-payment-api || true
	docker rm finguard-payment-api || true

payment-api-compose-up:
	cd services/payment-api && docker compose up --build -d

payment-api-compose-down:
	cd services/payment-api && docker compose down

payment-api-trivy-scan:
	trivy image --severity HIGH,CRITICAL --ignore-unfixed finguard/payment-api:phase-2
