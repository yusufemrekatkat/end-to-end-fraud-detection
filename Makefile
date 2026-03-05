.PHONY: install test lint train serve docker-build docker-up

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check .

train:
	python -m fraud_detection.training.trainer

serve:
	uvicorn fraud_detection.serving.api:app --reload

docker-build:
	docker compose -f docker/docker-compose.yml build

docker-up:
	docker compose -f docker/docker-compose.yml up serve