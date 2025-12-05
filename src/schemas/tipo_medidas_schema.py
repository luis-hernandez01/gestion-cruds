from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class tipo_medidaSchema(BaseModel):
    id: int
    nombre: str

class tipo_medidaCreate(BaseModel):
    nombre: str

class tipo_medidaUpdate(BaseModel):
    nombre: str

class AlcanceResponse(tipo_medidaSchema):
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
    items: List[tipo_medidaSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

