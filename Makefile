.PHONY: format lint test up down migrate makemigrations

format:
	black src
	isort src

lint:
	flake8 src

test:
	pytest --cov=src

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	python manage.py migrate_schemas --shared

makemigrations:
	python manage.py makemigrations
