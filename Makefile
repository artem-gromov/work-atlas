.PHONY: format lint test up down migrate makemigrations

format:
	pre-commit run --files $(shell git ls-files '*.py')

lint:
	flake8 src

test:
	pytest -q

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	python manage.py migrate_schemas --shared

makemigrations:
	python manage.py makemigrations

