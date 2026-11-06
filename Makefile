.PHONY: setup login pull up down restart logs ps clean

setup:
	@test -f .env || (cp .env.example .env && echo ".env criado: edite com seus dados")

login:
	@echo "Use um PAT com read:packages se a imagem for privada:"
	docker login ghcr.io

pull:
	docker compose pull api

up: setup pull
	docker compose up -d
	docker compose ps

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down -v
