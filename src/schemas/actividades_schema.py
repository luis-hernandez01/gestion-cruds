from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ActividadSchema(BaseModel):
    id: int
    nombre: str

class ActividadCreate(BaseModel):
    nombre: str

class ActividadUpdate(BaseModel):
    nombre: str

class AlcanceResponse(ActividadSchema):
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
    items: List[ActividadSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

