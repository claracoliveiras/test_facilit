from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import Evento, EventoCreate, EventoUpdate
from app.services import evento_service

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.post("", response_model=Evento, status_code=status.HTTP_201_CREATED)
def criar_evento(payload: EventoCreate, db: Session = Depends(get_db)):
    try:
        return evento_service.criar_evento(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade ao criar evento")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro de banco de dados")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao criar evento")


@router.get("", response_model=list[Evento])
def listar_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return evento_service.listar_eventos(db, skip=skip, limit=limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro de banco de dados")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao listar eventos")


@router.get("/{evento_id}", response_model=Evento)
def buscar_evento(evento_id: UUID, db: Session = Depends(get_db)):
    try:
        db_evento = evento_service.buscar_evento(db, evento_id)
        if not db_evento:
            raise HTTPException(status_code=404, detail="Evento nao encontrado")
        return db_evento
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro de banco de dados")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao buscar evento")


@router.put("/{evento_id}", response_model=Evento)
def atualizar_evento(evento_id: UUID, payload: EventoUpdate, db: Session = Depends(get_db)):
    try:
        db_evento = evento_service.atualizar_evento(db, evento_id=evento_id, payload=payload)
        if not db_evento:
            raise HTTPException(status_code=404, detail="Evento nao encontrado")
        return db_evento
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade ao atualizar evento")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro de banco de dados")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar evento")


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_evento(evento_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted = evento_service.deletar_evento(db, evento_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Evento nao encontrado")
        return None
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro de banco de dados")
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao deletar evento")
