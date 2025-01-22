.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000
ENV_FILE ?= .local.env

run: ## Run the application using uvicorn with provided arguments or defaults
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload 

# --env-file $(ENV_FILE)

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

update-poetry: ## Update poetry package
	pip install --upgrade poetry

migrate-create: 
	alembic revision --autogenerate -m "$(MIGRATION)"

migrate-apply:
	alembic upgrade head

migrate-revert:
	alembic downgrate -1

docker-up: ## docker compose up -d
	docker compose up -d

docker-down: ## docker compose down
	docker compose down

celery: ## start celery process
	celery -A app.tasks.celery_app:celery_app worker --loglevel=INFO

celery-beat: ## start celery beat process
	celery -A app.tasks.celery_app:celery_app worker --loglevel=INFO -B

celery-flower: ## start flower
	celery -A app.tasks.celery_app:celery_app flower

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'