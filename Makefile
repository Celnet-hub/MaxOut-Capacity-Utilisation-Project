VENV_PYTHON := .venv/bin/python
VENV_PIP := .venv/bin/pip

.PHONY: help install install-dev editable init-db seed-db run-api dev lint test

help:
	@echo "Available targets:"
	@echo "  make install     - install dependencies from requirements.txt"
	@echo "  make install-dev - install production and development dependencies"
	@echo "  make editable    - install project in editable mode"
	@echo "  make init-db     - create database tables"
	@echo "  make seed-db     - seed database with mock data"
	@echo "  make run-api     - run FastAPI app with python -m"
	@echo "  make dev         - run FastAPI app with uvicorn autoreload"
	@echo "  make lint        - run ruff linter and formatter checks"
	@echo "  make test        - run pytest suite"

install:
	$(VENV_PIP) install -r requirements.txt

install-dev: install
	$(VENV_PIP) install -r requirements-dev.txt

editable:
	$(VENV_PIP) install -e .

init-db:
	$(VENV_PYTHON) -m init_db

seed-db:
	$(VENV_PYTHON) -m seed_db

run-api:
	$(VENV_PYTHON) -m middleware.main

dev:
	$(VENV_PYTHON) -m uvicorn middleware.main:app --reload

lint:
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m ruff format --check .

test:
	$(VENV_PYTHON) -m pytest -v

