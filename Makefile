.PHONY: help setup test lint format check clean run

# Define variables
PYTHON = python3
VENV = venv
BIN = $(VENV)/bin

# Colors for pretty printing
BLUE = \033[0;34m
NC = \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "${BLUE}make setup${NC}  : Create virtual environment and install dependencies"
	@echo "${BLUE}make test${NC}   : Run all tests"
	@echo "${BLUE}make lint${NC}   : Run linter (Ruff)"
	@echo "${BLUE}make format${NC} : Format code with Ruff"
	@echo "${BLUE}make check${NC}  : Run linter and formatter check without making changes"
	@echo "${BLUE}make clean${NC}  : Remove virtual environment and cache files"
	@echo "${BLUE}make run${NC}    : Run the main application"

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

test:
	$(BIN)/python -m unittest discover tests

lint:
	$(BIN)/ruff check .

format:
	$(BIN)/ruff format .

check:
	$(BIN)/ruff check .
	$(BIN)/ruff format . --check

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

run:
	$(BIN)/python main.py