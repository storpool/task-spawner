# Image name and tag
IMAGE_NAME=cts.storpool.com/ticket-spawner/release
TAG=latest

# Helm chart directory
HELM_CHART = charts/ticket-spawner

# Docker build context
CONTEXT=.

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) $(CONTEXT)

# Push the image to the container registry
push: build
	docker push $(IMAGE_NAME):$(TAG)

# Clean up dangling images
clean:
	docker image prune -f

# Rebuild and push
release: clean push

helm-lint:
	helm lint $(HELM_CHART)

helm-template:
	helm template $(HELM_CHART)

helm-upgrade:
	helm upgrade --install ticket-spawner $(HELM_CHART) -f $(HELM_CHART)/values.yaml --namespace ticket-spawner --create-namespace
