from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class EventoBase(BaseModel):
    data_inicio: date
    data_fim: date
    evento: str
    periodicidade: str
    departamento: str
    descricao: str
    engajamento: int | None = None
    alcance: int | None = None
    status: str

    @model_validator(mode="after")
    def validar_periodo(self):
        if self.data_fim <= self.data_inicio:
            raise ValueError("data_fim deve ser maior que data_inicio")
        return self


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    pass


class Evento(EventoBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    criado_em: datetime
