.PHONY: help install test lint format clean run docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linters (flake8, mypy)"
	@echo "  make format       - Format code (black, isort)"
	@echo "  make clean        - Remove generated files"
	@echo "  make run          - Run the assistant"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

test:
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

test-fast:
	pytest tests/ -v

lint:
	flake8 app/ tests/ --max-line-length=100 --ignore=E203,W503
	mypy app/ --config-file=mypy.ini

format:
	black app/ tests/ main.py --line-length=100
	isort app/ tests/ main.py --profile=black

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/ dist/ build/

run:
	python main.py

docker-build:
	docker build -t jarvis-assistant .

docker-run:
	docker-compose up

docker-down:
	docker-compose down

docker-rebuild:
	docker-compose up --build
