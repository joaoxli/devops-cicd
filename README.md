# CI/CD com Containers

API Python (Flask) + MySQL + Nginx, empacotada em Docker, com pipeline no GitHub Actions
que publica a imagem no GitHub Packages (ghcr.io) e deploy via Docker Compose numa VM do Azure.

```
Código (GitHub) -> GitHub Actions -> GitHub Packages (ghcr.io) -> VM Azure (Docker Compose)
Cloudflare (DNS, HTTP 80) -> Nginx -> API Flask -> MySQL
```

## Endpoints
- `GET /` informações do projeto
- `GET /health` status da API e do banco
- `GET /recados` lista recados
- `POST /recados` cria recado: `{"autor": "Fulano", "mensagem": "Oi"}`

## Comandos (Makefile)
`make up` | `make down` | `make logs` | `make ps` | `make restart` | `make clean`

## Deploy
1. Crie `.env` a partir de `.env.example` e ajuste `API_IMAGE` e as senhas.
2. `make up`
