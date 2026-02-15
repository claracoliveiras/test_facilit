from fastapi import FastAPI

from app.api.routes import eventos_router
from app.core.db import Base, engine
from app import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Facilit API", version="1.0.0")
app.include_router(eventos_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
