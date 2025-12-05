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

@router.get("/{schema}/all")
def list_all(schema: str, 
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return CombustibleService(db, schema).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/{schema}/", response_model=PaginacionSchema)
def listar(schema: str, 
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


@router.post("/{schema}/")
def create(schema: str, 
    request: Request,
    payload: CombustibleCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = CombustibleService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{combustible_id}")
def get_show(schema: str, combustible_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return CombustibleService(db, schema).show(combustible_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{combustible_id}")
def update(schema: str, 
    request: Request,
    combustible_id: int,
    payload: CombustibleUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = CombustibleService(db, schema).update(combustible_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{combustible_id}")
def delete(schema: str, 
    request: Request,
    combustible_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = CombustibleService(db, schema).delete(combustible_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/{combustible_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        combustible_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = CombustibleService(db, schema).reactivate(combustible_id, request, tokenpayload)
    return {"data": result}