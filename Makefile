.PHONY: phase0-check tree docker-check kind-smoke-test kind-smoke-delete git-status

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
