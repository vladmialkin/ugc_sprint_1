up:
	docker compose up -d --build

down:
	docker compose down -v

lint:
	ruff format .
	ruff check . --fix --show-fixes

.DEFAULT_GOAL := up
