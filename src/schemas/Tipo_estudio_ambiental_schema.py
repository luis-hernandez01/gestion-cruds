from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Tipo_estudio_ambientalSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class Tipo_estudio_ambientalCreate(BaseModel):
    nombre: str


class Tipo_estudio_ambientalUpdate(BaseModel):
    nombre: str


class Tipo_estudio_ambientalResponse(Tipo_estudio_ambientalSchema):
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
    items: List[Tipo_estudio_ambientalSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
