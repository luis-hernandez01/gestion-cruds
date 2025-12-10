from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.factor_emisiones_services import FactoremisionService
from src.schemas.factores_emision_schema import (PaginacionSchema, 
                                                FactoremisionCreate,
                                                FactoremisionUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/factores_emisiones/all")
def list_all(schema: Optional[str], request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return FactoremisionService(db, schema).all()


# endpoint de listar data con paginacion incluida
@router.get("/{schema}/factores_emisiones/", response_model=PaginacionSchema)
def lista(schema: Optional[str], request: Request,
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
    schema = request.state.schema
    skip = (page - 1) * per_page
    limit = per_page
    data = FactoremisionService(db, schema).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = FactoremisionService(db, schema).count(activo=activo, filtros=filtros)  
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
@router.post("/{schema}/factores_emisiones/")
def creates(schema: Optional[str], request: Request, 
                        payload: FactoremisionCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = FactoremisionService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/factores_emisiones/{factor_id}")
def get_show(schema: Optional[str], request: Request, factor_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return FactoremisionService(db, schema).show(factor_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/factores_emisiones/{factor_id}")
def update(schema: Optional[str], request: Request, 
                        factor_id: int,
                        payload: FactoremisionUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = FactoremisionService(db, schema).updates(factor_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/factores_emisiones/{factor_id}")
def delete(schema: Optional[str], request: Request, 
                        factor_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = FactoremisionService(db, schema).deletes(factor_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/factores_emisiones/{factor_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        factor_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = FactoremisionService(db, schema).reactivate(factor_id, request, tokenpayload)
    return {"data": result}