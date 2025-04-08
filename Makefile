# Image name and tag
IMAGE_NAME=cts.storpool.com/ticket-spawner/release
TAG=latest

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
