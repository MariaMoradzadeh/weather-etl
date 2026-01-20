.PHONY: help up down logs psql schema run fmt lint

help:
	@echo "Commands:"
	@echo "  make up        Start Postgres (docker compose up -d)"
	@echo "  make down      Stop containers"
	@echo "  make logs      Tail container logs"
	@echo "  make psql      Open psql shell in the db container"
	@echo "  make schema    Apply schema.sql to the database"
	@echo "  make run       Run the ETL pipeline"
	@echo "  make fmt       Format (ruff)"
	@echo "  make lint      Lint (ruff)"
	@echo "  make precommit-install  Install pre-commit hooks"
	@echo "  make precommit          Run pre-commit on all files"
	@echo "  make check              Run lint + pre-commit"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

psql:
	docker compose exec db psql -U etl -d etldb

schema:
	docker compose exec -T db psql -U etl -d etldb -f sql/schema.sql

run:
	python -m src.run_pipeline

fmt:
	python -m pip install -q ruff
	ruff format .

lint:
	python -m pip install -q ruff
	ruff check .
	

precommit-install:
	python -m pip install -q pre-commit ruff
	pre-commit install

precommit:
	python -m pip install -q pre-commit ruff
	pre-commit run --all-files
check:
	$(MAKE) lint
	$(MAKE) precommit


