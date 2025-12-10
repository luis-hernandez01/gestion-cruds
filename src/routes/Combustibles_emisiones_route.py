from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import get_session
from src.schemas.Combustibles_emisiones_schema import (
    CombustibleCreate,
    PaginacionSchema,
    CombustibleUpdate,
)
from src.services.combustibles_emision_services import CombustibleService
from src.utils.jwt_validator_util import verify_jwt_token
from src.config.config import (get_db)



# inicializacion del roter
router = APIRouter()


# mostrar todo 

@router.get("/{schema}/combustibles_emision/all")
def list_all(schema: Optional[str], request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return CombustibleService(db, schema).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/{schema}/combustibles_emision/", response_model=PaginacionSchema)
def listar(schema: Optional[str], request: Request,
    activo: Optional[bool] = Query(True, description="Filtrar por activo (true o false)"),
    filtros: Optional[str] = Query(
        None,
        description="Filtrar por nombre (búsqueda parcial)"
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
) -> Dict[str, Any]:
    schema = request.state.schema
    skip = (page - 1) * per_page
    limit = per_page
    data = CombustibleService(db, schema).lista(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = CombustibleService(db, schema).count(activo=activo, filtros=filtros)
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


@router.post("/{schema}/combustibles_emision/")
def create(schema: Optional[str], 
    request: Request,
    payload: CombustibleCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    result = CombustibleService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/combustibles_emision/{combustible_id}")
def get_show(schema: Optional[str], request: Request, combustible_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return CombustibleService(db, schema).show(combustible_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/combustibles_emision/{combustible_id}")
def update(schema: Optional[str], 
    request: Request,
    combustible_id: int,
    payload: CombustibleUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    result = CombustibleService(db, schema).update(combustible_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/combustibles_emision/{combustible_id}")
def delete(schema: Optional[str], 
    request: Request,
    combustible_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    result = CombustibleService(db, schema).delete(combustible_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/combustibles_emision/{combustible_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        combustible_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = CombustibleService(db, schema).reactivate(combustible_id, request, tokenpayload)
    return {"data": result}