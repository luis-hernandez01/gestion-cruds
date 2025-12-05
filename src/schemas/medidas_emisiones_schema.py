from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class medidasemisionSchema(BaseModel):
    id: int
    valores: Optional[Decimal] = None
    id_tipomedida: Optional[int]

class medidasemisionCreate(BaseModel):
    valores: Optional[Decimal] = None
    id_tipomedida: Optional[int]

class medidasemisionUpdate(BaseModel):
    valores: Optional[Decimal] = None
    id_tipomedida: Optional[int]

class AlcanceResponse(medidasemisionSchema):
    id: int

class LogEntityRead(BaseModel):
    id: int
    valores: Optional[Decimal] = None
    id_tipomedida: Optional[int]
    id_persona: Optional[int]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    items: List[medidasemisionSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int

