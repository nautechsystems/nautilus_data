PROJECT?= 				nautechsystems/nautilus_data
REGISTRY?= 				ghcr.io/
IMAGE?= 				${REGISTRY}${PROJECT}
GIT_TAG:= 				$(shell git rev-parse --abbrev-ref HEAD)
IMAGE_FULL?=			${IMAGE}:${GIT_TAG}
PYTHON_EXECUTABLE:= 	$(shell which python3)
NAUTILUS_DATA:=			"${HOME}/.nautilus"

########################################
#  Docker development commands
########################################
docker-build:
	(docker pull ${IMAGE} || true)
	(docker build --platform linux/x86_64 -t ${IMAGE_FULL} .)

docker-build-force:
	(docker build --no-cache -t ${IMAGE_FULL} ./.. )

docker-push:
	(docker push ${BACKEND_IMAGE_FULL} )

########################################
# Development commands
########################################

poetry-update:
	(poetry update)

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .mypy_cache
	rm -rf .nox
	rm -rf .pytest_cache
	rm -rf nautilus_platform/.mypy_cache
	rm -rf nautilus_platform/.nox
	rm -rf nautilus_platform/.pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf docs/build
	find . -name dask-worker-space -type d -exec rm -rf {} +
	find . -name .benchmarks -type d -exec rm -rf {} +
	find . -name '*.dll' -exec rm {} +
	find . -name '*.prof' -exec rm {} +
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +
	find . -name '*.so' -exec rm {} +
	find . -name '*.o' -exec rm {} +
	find . -name '*.c' -exec rm {} +
	rm -f coverage.xml
	rm -f dump.rdb
