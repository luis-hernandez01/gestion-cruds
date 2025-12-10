from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.alcance_services import AlcanceService
from src.schemas.Alcance_fuentefija_schema import (PaginacionSchema, 
                                                AlcanceCreate,
                                                AlcanceUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/alcance_funtefija/all")
def list_all(schema: Optional[str], request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return AlcanceService(db, schema).all()


# endpoint de listar data con paginacion incluida
@router.get("/{schema}/alcance_funtefija/", response_model=PaginacionSchema)
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
    data = AlcanceService(db, schema).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = AlcanceService(db, schema).count(activo=activo, filtros=filtros)  
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
@router.post("/{schema}/alcance_funtefija/")
def creates(schema: Optional[str], request: Request, 
                        payload: AlcanceCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = AlcanceService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/alcance_funtefija/{alcance_id}")
def get_show(schema: Optional[str], alcance_id: int, request: Request,
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return AlcanceService(db, schema).show(alcance_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/alcance_funtefija/{alcance_id}")
def update(schema: Optional[str], request: Request, 
                        alcance_id: int,
                        payload: AlcanceUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = AlcanceService(db, schema).updates(alcance_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/alcance_funtefija/{alcance_id}")
def delete(schema: Optional[str], request: Request, 
                        alcance_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = AlcanceService(db, schema).deletes(alcance_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/alcance_funtefija/{alcance_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        alcance_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = AlcanceService(db, schema).reactivate(alcance_id, request, tokenpayload)
    return {"data": result}