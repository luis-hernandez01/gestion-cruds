from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Periosidad_informeSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class Periosidad_informeCreate(BaseModel):
    nombre: str


class Periosidad_informeUpdate(BaseModel):
    nombre: str


class TPeriosidad_informeResponse(Periosidad_informeSchema):
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
    items: List[Periosidad_informeSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
