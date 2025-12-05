from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FactoremisionSchema(BaseModel):
    id: int
    N2O_kg_gal: Optional[Decimal] = None
    CO2_kg_gal: Optional[Decimal] = None
    CH4_kg_km: Optional[Decimal] = None
    
    activo: bool


class FactoremisionCreate(BaseModel):
    id_tipofuente: Optional[int] = None
    id_equipoproceso: Optional[int] = None
    id_categoria: Optional[int] = None
    id_Combustible: Optional[int] = None
    
    N2O_kg_gal: Optional[Decimal] = None
    CO2_kg_gal: Optional[Decimal] = None
    CH4_kg_km: Optional[Decimal] = None

    id_unidades_factor_emision: Optional[int] = None


class FactoremisionUpdate(BaseModel):
    id_tipofuente: Optional[int] = None
    id_equipoproceso: Optional[int] = None
    id_categoria: Optional[int] = None
    id_Combustible: Optional[int] = None
    
    N2O_kg_gal: Optional[Decimal] = None
    CO2_kg_gal: Optional[Decimal] = None
    CH4_kg_km: Optional[Decimal] = None

    id_unidades_factor_emision: Optional[int] = None


class FactoremisionResponse(FactoremisionSchema):
    id: int


class LogEntityRead(BaseModel):
    id: int
    
    id_tipofuente: Optional[int] = None
    id_equipoproceso: Optional[int] = None
    id_categoria: Optional[int] = None
    id_Combustible: Optional[int] = None
    
    N2O_kg_gal: Optional[Decimal] = None
    CO2_kg_gal: Optional[Decimal] = None
    CH4_kg_km: Optional[Decimal] = None

    id_unidades_factor_emision: Optional[int] = None
    
    
    id_persona: Optional[int]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginacionSchema(BaseModel):
    items: List[FactoremisionSchema]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
