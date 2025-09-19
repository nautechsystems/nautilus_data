# Variables
# -----------------------------------------------------------------------------
PROJECT?=nautechsystems/nautilus_data
REGISTRY?=ghcr.io/
IMAGE?=$(REGISTRY)$(PROJECT)
GIT_TAG:=$(shell git rev-parse --abbrev-ref HEAD)
IMAGE_FULL?=$(IMAGE):$(GIT_TAG)

V = 0  # 0 / 1 - verbose mode
Q = $(if $(filter 1,$V),,@) # Quiet mode, suppress command output
M = $(shell printf "$(BLUE)>$(RESET)") # Message prefix for commands

# > Colors
RED    := $(shell tput -Txterm setaf 1)
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
BLUE   := $(shell tput -Txterm setaf 4)
PURPLE := $(shell tput -Txterm setaf 5)
CYAN   := $(shell tput -Txterm setaf 6)
GRAY   := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.DEFAULT_GOAL := help

#== Installation

.PHONY: install
install:  #-- Install dependencies using uv
	$(info $(M) Installing dependencies...)
	$Q uv sync

.PHONY: install-dev
install-dev:  #-- Install all development dependencies
	$(info $(M) Installing development dependencies...)
	$Q uv sync --all-groups

.PHONY: update
update:  #-- Update dependencies using uv
	$(info $(M) Updating dependencies...)
	$Q uv sync --upgrade

#== Clean

.PHONY: clean
clean: clean-caches  #-- Clean all caches and build artifacts
	$(info $(M) Cleaning all caches and build artifacts...)
	$Q rm -rf dist build 2>/dev/null || true

.PHONY: clean-caches
clean-caches:  #-- Clean pytest, mypy, ruff, and uv caches
	$Q rm -rf .pytest_cache .mypy_cache .ruff_cache 2>/dev/null || true
	$Q find . -type d -name "__pycache__" -not -path "./.venv*" -print0 | xargs -0 -r rm -rf
	$Q find . -type f -name "*.pyc" -not -path "./.venv*" -print0 | xargs -0 -r rm -f

.PHONY: distclean
distclean: clean  #-- Nuclear clean - remove all untracked files (requires FORCE=1)
	@[ "$$FORCE" = 1 ] || { echo "Pass FORCE=1 to really nuke"; exit 1; }
	@echo "⚠️  nuking working tree (git clean -fxd)…"
	git clean -fxd

#== Code Quality

.PHONY: format
format:  #-- Format code using ruff
	$(info $(M) Formatting code with ruff...)
	$Q uv run --no-sync ruff format .

.PHONY: pre-commit
pre-commit:  #-- Run all pre-commit hooks on all files
	$(info $(M) Running pre-commit hooks...)
	$Q uv run --no-sync pre-commit run --all-files

.PHONY: ruff
ruff:  #-- Run ruff linter with automatic fixes
	$(info $(M) Running ruff linter with fixes...)
	$Q uv run --no-sync ruff check . --fix

.PHONY: mypy
mypy:  #-- Run mypy static type checker
	$(info $(M) Running mypy type checker...)
	$Q uv run --no-sync mypy .

#== Testing

.PHONY: pytest
pytest:  #-- Run Python tests with pytest
	$(info $(M) Running pytest...)
	$Q uv run --no-sync pytest

#== Docker

.PHONY: docker-build
docker-build:  #-- Build Docker image
	$(info $(M) Building Docker image $(IMAGE_FULL)...)
	$Q docker pull $(IMAGE) || true
	$Q docker build --platform linux/x86_64 -t $(IMAGE_FULL) .

.PHONY: docker-build-force
docker-build-force:  #-- Force rebuild Docker image without cache
	$(info $(M) Force rebuilding Docker image $(IMAGE_FULL)...)
	$Q docker build --no-cache -t $(IMAGE_FULL) .

.PHONY: docker-push
docker-push:  #-- Push Docker image to registry
	$(info $(M) Pushing Docker image $(IMAGE_FULL)...)
	$Q docker push $(IMAGE_FULL)

#== Help

.PHONY: help
help:  #-- Show this help message
	@echo "$(CYAN)Nautilus Data Makefile$(RESET)"
	@echo ""
	@echo "$(YELLOW)Usage:$(RESET)"
	@echo "  make [target] [V=1] [OPTION=value]"
	@echo ""
	@echo "$(YELLOW)Available targets:$(RESET)"
	@grep -E '^[a-zA-Z0-9_%/-]+:.*#--' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*#--"}; \
		{gsub(/^[^:]*:/, "", $$1); \
		printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Options:$(RESET)"
	@echo "  $(BLUE)V=1$(RESET)              Enable verbose output"
	@echo "  $(BLUE)FORCE=1$(RESET)          Required for distclean target"
