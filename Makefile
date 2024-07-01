SOURCE_DIR = http_kit
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
.DEFAULT_GOAL := all
PROJECT_VERSION ?= v$(shell poetry version -s)

format:
	poetry run black $(PROJECT_DIRS)
	poetry run isort $(PROJECT_DIRS)

lint:
	poetry run ruff check $(SOURCE_DIR)
	poetry run mypy --install-types --show-error-codes --non-interactive $(SOURCE_DIR)

test:
	poetry run pytest

fix:
	poetry run black $(PROJECT_DIRS)
	poetry run isort $(PROJECT_DIRS)
	poetry run ruff check $(SOURCE_DIR) --fix

all: format lint test

version:
	poetry version minor
