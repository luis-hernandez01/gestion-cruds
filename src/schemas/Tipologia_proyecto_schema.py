from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Tipologia_proyectoSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class Tipologia_proyectoCreate(BaseModel):
    nombre: str


class Tipologia_proyectoUpdate(BaseModel):
    nombre: str


class Tipologia_proyectoResponse(Tipologia_proyectoSchema):
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
    items: List[Tipologia_proyectoSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
