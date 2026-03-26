VENV_PYTHON := .venv/bin/python
VENV_PIP := .venv/bin/pip

.PHONY: help install editable init-db seed-db run-api dev

help:
	@echo "Available targets:"
	@echo "  make install    - install dependencies from requirements.txt"
	@echo "  make editable   - install project in editable mode"
	@echo "  make init-db    - create database tables"
	@echo "  make seed-db    - seed database with mock data"
	@echo "  make run-api    - run FastAPI app with python -m"
	@echo "  make dev        - run FastAPI app with uvicorn autoreload"

install:
	$(VENV_PIP) install -r requirements.txt

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
