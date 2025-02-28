SHELL=/bin/bash
PROJECT_DIR=$(shell pwd)

init:
	@python3 -m venv venv
	@gcloud auth login
	@echo "[INFO] python virtual env created...please run source venv/bin/activate"
	@echo "[SUCCESS] initialization completed"

install:
	@pip install -e .

install-dev:
	@pip install -e ".[dev]"

format:
	@black .
