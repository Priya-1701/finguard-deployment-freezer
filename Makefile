.PHONY: phase0-check tree docker-check kind-smoke-test kind-smoke-delete git-status \
        payment-api-install payment-api-test payment-api-run payment-api-health payment-api-metrics

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
