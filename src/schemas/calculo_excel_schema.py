from pydantic import BaseModel
from typing import List, Optional, Any

class Emision4Item(BaseModel):
    PR_INICIAL: float
    PR_FINAL: float
    Trimestral: str
    codigo_via: str
    ID: Optional[Any] = None
    Tramo: str
    Actividad: str

class EmisionTrimestreItem(BaseModel):
    Trimestral: str
    Emisiones: float
    ID: Optional[Any] = None
    Tramo: str
