# Seminário DevOps – T02: Docker Compose

API Flask e banco Redis rodando como serviços conectados via Docker Compose, com persistência em volume.

## Objetivo e arquitetura

Mostrar dois serviços que se comunicam pela rede interna do Compose e que mantêm dados mesmo após recriar um container.

```
cliente --HTTP:5000--> [api (Flask)] --rede do Compose, host "redis":6379--> [redis] --> volume "meus-dados" (/data)
```

- **api**: Flask; a cada acesso a `/` incrementa a chave `visitas` no Redis e devolve uma página HTML com o contador (container `api_contador`).
- **redis**: `redis:7-alpine` com `--appendonly yes`, gravando em `/data`, montado no volume nomeado `meus-dados` (container `banco_redis`).

## Versões e requisitos

- Docker Engine 24+ e Docker Compose v2 (`docker compose`)
- Python 3.9 (imagem `python:3.9-alpine`), Flask 3.1.3 e redis-py 7.0.1 (fixados no `requirements.txt`)
- Redis 7 (`redis:7-alpine`)

**Versões testadas (12/11/2026, GitHub Codespaces):** Docker 29.9.2-2 e Docker Compose v5.6.1.

Dados fictícios: o único dado é um contador de visitas.

## Execução

```bash
cp .env.example .env   # opcional; os valores padrão já funcionam
docker compose up -d --build
```

## Verificação

1. Acessar a API: abrir `http://localhost:5000` no navegador (no Codespaces, pela aba **Portas**). A página mostra "Projeto DevOps - T02", o selo "API Online" e o contador de visitas.
   Pelo terminal, só o número: `curl -s localhost:5000 | grep -oE 'count-number">[0-9]+' | cut -d'>' -f2`
2. Atualizar a página algumas vezes e ver o contador subir.
3. **Recriar o container preservando os dados:**
   ```bash
   docker compose rm -sf redis      # remove o container do Redis
   docker compose up -d redis       # cria um novo container
   # atualizar a página: o contador continua de onde parou
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

## Slides da apresentação

- [Docker-Compose-T02.pptx](slides/Docker-Compose-T02.pptx): editável, com as notas de fala em cada slide.
- [Docker-Compose-T02.pdf](slides/Docker-Compose-T02.pdf): a mesma apresentação em PDF.

## Entrega

Versão entregue: tag `entrega-t02` (12/11/2026), atualizada no mesmo dia com as mudanças abaixo.

### Mudanças depois da primeira entrega (12/11/2026)

- `app.py`: a resposta passou de texto simples para uma página HTML com o contador de visitas.
- `docker-compose.yml`: nomes de container (`api_contador`, `banco_redis`) e `restart: unless-stopped`; removida a linha `version`, obsoleta no Compose v2; imagem do Redis mantida em `redis:7-alpine` com `--appendonly yes`.
- `.env.example`: só `REDIS_HOST`, a única variável que a API usa.
- `requirements.txt`: versões fixadas (`Flask==3.1.3`, `redis==7.0.1`), as que rodam na imagem.
- Slides (PPTX e PDF): a demonstração passou a abrir a página no navegador, no Codespaces.

## Autores

Equipe Galegos:

- Ítalo Waldecy Pereira dos Santos
- Hugo Duarte Dias
- Caio Gomes Ferrão D'avila
- Caetano Mesquita
- Helio Gomes Cunha
