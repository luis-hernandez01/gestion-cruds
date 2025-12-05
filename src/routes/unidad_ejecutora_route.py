from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import (get_db)
from src.schemas.unidad_ejecutora_schema import (
    UnidadEjecutoraCreate,
    PaginacionSchema,
    UnidadEjecutoraUpdate,
)
from src.services.unidad_ejecutora_services import UnidadEjecutoraService
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
    return UnidadEjecutoraService(db, schema).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/{schema}/", response_model=PaginacionSchema)
def list_unidades(schema: str, 
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
    data = UnidadEjecutoraService(db, schema).list_unidad_ejecutora(activo=activo, filtros=filtros,
                                                            skip=skip, limit=limit)
    total = UnidadEjecutoraService(db, schema).count_unidad_ejecutora(activo=activo, filtros=filtros)
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
def create_unidades(schema: str, 
    request: Request,
    payload: UnidadEjecutoraCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadEjecutoraService(db, schema).create_unidad(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{unidad_id}")
def get_show(schema: str, unidad_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return UnidadEjecutoraService(db, schema).show(unidad_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{unidad_id}")
def update_unidades(schema: str, 
    request: Request,
    unidad_id: int,
    payload: UnidadEjecutoraUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadEjecutoraService(db, schema).update_unidad(unidad_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{unidad_id}")
def delete_unidades(schema: str, 
    request: Request,
    unidad_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = UnidadEjecutoraService(db, schema).delete_unidad(unidad_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/{unidad_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        unidad_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = UnidadEjecutoraService(db, schema).reactivate(unidad_id, request, tokenpayload)
    return {"data": result}