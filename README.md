# Seminário DevOps – T02: Docker Compose

API Flask e banco Redis rodando como serviços conectados via Docker Compose, com persistência em volume.

## Objetivo e arquitetura

Mostrar dois serviços que se comunicam pela rede interna do Compose e que mantêm dados mesmo após recriar um container.

```
cliente --HTTP:5000--> [api (Flask)] --rede do Compose, host "redis":6379--> [redis] --> volume "meus-dados" (/data)
```

- **api**: Flask; a cada acesso a `/` incrementa a chave `visitas` no Redis.
- **redis**: `redis:7-alpine` com `--appendonly yes`, gravando em `/data`, montado no volume nomeado `meus-dados`.

## Versões e requisitos

- Docker Engine 24+ e Docker Compose v2 (`docker compose`)
- Python 3.9 (imagem `python:3.9-alpine`), Flask, redis-py
- Redis 7 (`redis:7-alpine`)

Dados fictícios: o único dado é um contador de visitas.

## Execução

```bash
cp .env.example .env   # opcional; os valores padrão já funcionam
docker compose up -d --build
```

## Verificação

1. Acessar a API: `curl http://localhost:5000` (ou abrir no navegador). Resposta: `A API foi acedida 1 vezes.`
2. Repetir algumas vezes e ver o contador subir.
3. **Recriar o container preservando os dados:**
   ```bash
   docker compose rm -sf redis      # remove o container do Redis
   docker compose up -d redis       # cria um novo container
   curl http://localhost:5000       # o contador continua de onde parou
   ```
4. Conferir o volume: `docker volume ls` (procure `meus-dados`).

## Limpeza

```bash
docker compose down        # remove containers e rede, mantém o volume
docker compose down -v     # remove também o volume (apaga os dados)
```

## Limitações

- Redis é um banco chave-valor em memória com persistência em disco; não substitui um banco relacional.
- Sem autenticação no Redis e com a porta 6379 exposta: aceitável só em demonstração local.
- O servidor de desenvolvimento do Flask não é indicado para produção.
- Não há testes automatizados.

## Fontes

- Docker Compose: https://docs.docker.com/compose/
- Redis persistence: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Flask: https://flask.palletsprojects.com/

## Autores

Preencher com os nomes da equipe.
