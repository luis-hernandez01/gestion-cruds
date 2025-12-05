from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import (get_db)
from src.schemas.Unidades_factores_emision_schema import (
    UnidadFactorCreate,
    PaginacionSchema,
    UnidadFactorUpdate,
)
from src.services.unidades_factor_emision_services import UnidadfactorService
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


# mostrar todo 

@router.get("/{schema}/all")
def list_all(schema: str, 
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return UnidadfactorService(db, schema).all()
    

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
    data = UnidadfactorService(db, schema).lista(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = UnidadfactorService(db, schema).count(activo=activo, filtros=filtros,)
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
    payload: UnidadFactorCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{unidadfactor_id}")
def get_show(schema: str, unidadfactor_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return UnidadfactorService(db, schema).show(unidadfactor_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{unidadfactor_id}")
def update_unidades(schema: str, 
    request: Request,
    unidadfactor_id: int,
    payload: UnidadFactorUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(db, schema).update(unidadfactor_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{unidadfactor_id}")
def delete(schema: str, 
    request: Request,
    unidadfactor_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadfactorService(db, schema).delete(unidadfactor_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/{unidadfactor_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        unidadfactor_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = UnidadfactorService(db, schema).reactivate(unidadfactor_id, request, tokenpayload)
    return {"data": result}