from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Evento
from app.schemas import EventoCreate, EventoUpdate


def criar_evento(db: Session, payload: EventoCreate) -> Evento:
    try:
        db_evento = Evento(
            data_inicio=payload.data_inicio,
            data_fim=payload.data_fim,
            evento=payload.evento,
            descricao=payload.descricao,
            engajamento=payload.engajamento,
            status=payload.status,
        )
        db.add(db_evento)
        db.commit()
        db.refresh(db_evento)
        return db_evento
    except SQLAlchemyError:
        db.rollback()
        raise


def listar_eventos(db: Session, skip: int = 0, limit: int = 100) -> list[Evento]:
    try:
        return db.query(Evento).offset(skip).limit(limit).all()
    except SQLAlchemyError:
        raise


def buscar_evento(db: Session, evento_id: UUID) -> Evento | None:
    try:
        return db.query(Evento).filter(Evento.id == evento_id).first()
    except SQLAlchemyError:
        raise


def atualizar_evento(db: Session, evento_id: UUID, payload: EventoUpdate) -> Evento | None:
    try:
        db_evento = buscar_evento(db, evento_id)
        if not db_evento:
            return None

        db_evento.data_inicio = payload.data_inicio
        db_evento.data_fim = payload.data_fim
        db_evento.evento = payload.evento
        db_evento.descricao = payload.descricao
        db_evento.engajamento = payload.engajamento
        db_evento.status = payload.status

        db.commit()
        db.refresh(db_evento)
        return db_evento
    except SQLAlchemyError:
        db.rollback()
        raise


def deletar_evento(db: Session, evento_id: UUID) -> bool:
    try:
        db_evento = buscar_evento(db, evento_id)
        if not db_evento:
            return False

        db.delete(db_evento)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
