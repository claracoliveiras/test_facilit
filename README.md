# FastAPI CRUD

## Project structure

```text
app/
  api/
    routes/
      eventos.py
  core/
    db.py
  models/
    evento.py
  schemas/
    evento.py
  services/
    evento_service.py
  main.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Database

This project uses PostgreSQL by default, reading values from `.env`:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

Optional values:
- `POSTGRES_HOST` (default: `localhost`)
- `POSTGRES_PORT` (default: `5432`)
- `DATABASE_URL` (overrides everything if provided)

## Endpoints

- `GET /health`
- `POST /eventos`
- `GET /eventos`
- `GET /eventos/{evento_id}`
- `PUT /eventos/{evento_id}`
- `DELETE /eventos/{evento_id}`
