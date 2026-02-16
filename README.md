# Facilit Test

Este repositório reúne uma aplicação de gestão de eventos, composta por uma API em FastAPI, banco de dados PostgreSQL e fluxos de automação no n8n, que contém um agente de inteligência artificial que consome as informações da API que consta nesse repositório. 

## Setup inicial

### Pré-requisitos:
- Docker Desktop
- Esse projeto utiliza as portas `8000`, `5678`, `5433`.


 É possível acessar os arquivos docker-compose e Dockerfile para modificar as portas caso necessário, atentando-se para modificar também os fluxos.

### .env

``` bash
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST

N8N_ENCRYPTION_KEY
```
### Docker
Na pasta principal do projeto, executar o seguinte comando que deve criar os containers necessários:

```bash
docker compose up --build -d
```

Acessos:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- n8n: `http://localhost:5678`
- PostgreSQL (host): `localhost:5433`

## Configurar n8n

### 1. Importar workflows

Importe no n8n:
- `n8n/Migração de dados.json`
- `n8n/Consulta com IA.json`

### 2. Configurar credenciais

- `Google Sheets account` (Google Sheets OAuth2) para o workflow **Migração de dados**
- `OpenAi account` (OpenAI API) para o workflow **Consulta com IA**

O workflow de migração de dados foi construído para ser executado **manualmente** de acordo com as planilhas conectadas, enquanto o workflow de Consulta funciona via **Webhook**.

## Webhook

Workflow: **Consulta com IA**
- A url para esse webhook pode ser encontrada no node inicial do fluxo.

Parâmetros esperados:
- `mensagem`
- `chatid`

Exemplo:

```bash
curl -X POST "http://localhost:5678/webhook/consulta-com-ia?mensagem=Liste%20os%20eventos&chatid=123"
```
