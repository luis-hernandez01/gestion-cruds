from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.ciclo_vida_services import CiclovidaService
from src.schemas.Ciclo_vida_schema import (PaginacionSchema, 
                                                Ciclo_vidaCreate,
                                                Ciclo_vidaUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/ciclo_vida/all")
def list_all(schema: Optional[str], request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return CiclovidaService(db, schema).all()


# endpoint de listar data con paginacion incluida
@router.get("/{schema}/ciclo_vida/", response_model=PaginacionSchema)
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
    data = CiclovidaService(db, schema).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = CiclovidaService(db, schema).count(activo=activo, filtros=filtros)  
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
@router.post("/{schema}/ciclo_vida/")
def creates(schema: Optional[str], request: Request, 
                        payload: Ciclo_vidaCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = CiclovidaService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/ciclo_vida/{ciclo_vida_id}")
def get_show(schema: Optional[str], request: Request, ciclo_vida_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return CiclovidaService(db, schema).show(ciclo_vida_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/ciclo_vida/{ciclo_vida_id}")
def update(schema: Optional[str], request: Request, 
                        ciclo_vida_id: int,
                        payload: Ciclo_vidaUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = CiclovidaService(db, schema).updates(ciclo_vida_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/ciclo_vida/{ciclo_vida_id}")
def delete(schema: Optional[str], request: Request, 
                        ciclo_vida_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = CiclovidaService(db, schema).deletes(ciclo_vida_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/ciclo_vida/{ciclo_vida_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        ciclo_vida_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = CiclovidaService(db, schema).reactivate(ciclo_vida_id, request, tokenpayload)
    return {"data": result}