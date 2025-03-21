SHELL=/bin/bash
PROJECT_DIR=$(shell pwd)

setup:
	@python3 -m venv venv
	# TODO: add gcloud initial download and setup
	@echo "[INFO] python virtual env created...please run source venv/bin/activate"

init:
	@gcloud auth login
	@echo "[SUCCESS] initialization completed"

install:
	@pip3 install -e .

install-dev:
	@pip3 install -e ".[dev]"

format:
	@black .
