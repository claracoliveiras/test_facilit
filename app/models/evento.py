import uuid

from sqlalchemy import CheckConstraint, Column, Date, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.db import Base


class Evento(Base):
    __tablename__ = "Eventos"
    __table_args__ = (
        CheckConstraint("data_fim > data_inicio", name="ck_eventos_data_fim_maior_data_inicio"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    evento = Column(String(120), nullable=False)
    periodicidade = Column(String(50), nullable=False)
    departamento = Column(String(120), nullable=False)
    descricao = Column(String(255), nullable=False)
    engajamento = Column(Integer, nullable=True)
    alcance = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False)
