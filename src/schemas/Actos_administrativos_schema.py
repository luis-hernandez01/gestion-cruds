from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Actos_administrativoSchema(BaseModel):
    id: int
    nombre: str
    activo: bool


class Actos_administrativoCreate(BaseModel):
    nombre: str


class Actos_administrativoUpdate(BaseModel):
    nombre: str


class Actos_administrativoResponse(Actos_administrativoSchema):
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
    items: List[Actos_administrativoSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
