PROJECT?=nautechsystems/nautilus_data
REGISTRY?=ghcr.io/
IMAGE?=${REGISTRY}${PROJECT}
GIT_TAG:=$(shell git rev-parse --abbrev-ref HEAD)
IMAGE_FULL?=${IMAGE}:${GIT_TAG}
PYTHON_EXECUTABLE:=$(shell which python3)
NAUTILUS_PATH:="${HOME}/.nautilus"

########################################
#  Docker development commands
########################################
docker-build:
	(docker pull ${IMAGE} || true)
	(docker build --platform linux/x86_64 -t ${IMAGE_FULL} .)

docker-build-force:
	(docker build --no-cache -t ${IMAGE_FULL} ./.. )

docker-push:
	(docker push ${IMAGE_FULL} )

########################################
# Development commands
########################################

update:
	poetry update

pre-commit:
	pre-commit run --all-files

clean:
	git clean -fxd
