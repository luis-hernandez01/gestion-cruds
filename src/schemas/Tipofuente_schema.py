from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TipofuenteSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class TipofuenteCreate(BaseModel):
    nombre: str


class TipofuenteUpdate(BaseModel):
    nombre: str


class UnidadEjecutoraResponse(TipofuenteSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    nombre: str
    id_persona: Optional[int]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginacionSchema(BaseModel):
    items: List[TipofuenteSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
