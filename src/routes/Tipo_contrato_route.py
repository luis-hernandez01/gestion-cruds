from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.tipo_contrato_services import Tipo_contratoService
from src.schemas.Tipo_contrato_schema import (PaginacionSchema, 
                                                Tipo_contratoCreate,
                                                Tipo_contratoUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/all")
def list_all(schema: str, 
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return Tipo_contratoService(db, schema).all()


# endpoint de listar data con paginacion incluida
@router.get("/{schema}/", response_model=PaginacionSchema)
def lista(schema: str, 
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    filtros: Optional[str] = Query(
        None,
        description="Filtrar por nombre (búsqueda parcial)"
    ),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = Tipo_contratoService(db, schema).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = Tipo_contratoService(db, schema).count(activo=activo, filtros=filtros)  
    # Método adicional para contar todos los datos
    return {
        "items": data,
        "per_page": per_page,
        "size": limit,
        "total": total,
        "last_page" : (total + per_page - 1) // per_page,
        "page": page,
        "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        
    }
    
    # endpoin de crear registro
@router.post("/{schema}/")
def creates(schema: str, request: Request, 
                        payload: Tipo_contratoCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipo_contratoService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{tipo_contrato_id}")
def get_show(schema: str, tipo_contrato_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return Tipo_contratoService(db, schema).show(tipo_contrato_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{tipo_contrato_id}")
def update(schema: str, request: Request, 
                        tipo_contrato_id: int,
                        payload: Tipo_contratoUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipo_contratoService(db, schema).updates(tipo_contrato_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{tipo_contrato_id}")
def delete(schema: str, request: Request, 
                        tipo_contrato_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipo_contratoService(db, schema).deletes(tipo_contrato_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/{tipo_contrato_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        tipo_contrato_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipo_contratoService(db, schema).reactivate(tipo_contrato_id, request, tokenpayload)
    return {"data": result}