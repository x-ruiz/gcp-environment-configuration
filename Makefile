SHELL=/bin/bash
PROJECT_DIR=$(shell pwd)

init:
	@python3 -m venv venv

install:
	@pip install -e .

install-dev:
	@pip install -e ".[dev]"
