from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import (get_db)
from src.schemas.Tipologia_proyecto_schema import (
    Tipologia_proyectoCreate,
    PaginacionSchema,
    Tipologia_proyectoUpdate,
)
from src.services.tipologia_proyecto_services import Tipologia_proyectoService
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
    return Tipologia_proyectoService(db, schema).all()
    

# endpoint de listar data con paginacion incluida
@router.get("/{schema}/", response_model=PaginacionSchema)
def lista(schema: str, 
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
    data = Tipologia_proyectoService(db, schema).listar(activo=activo, filtros=filtros,
                                                            skip=skip, limit=limit)
    total = Tipologia_proyectoService(db, schema).count(activo=activo, filtros=filtros)
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
def creates(schema: str, 
    request: Request,
    payload: Tipologia_proyectoCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipologia_proyectoService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{tipologia_id}")
def get_show(schema: str, tipologia_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return Tipologia_proyectoService(db, schema).show(tipologia_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{tipologia_id}")
def update(schema: str, 
    request: Request,
    tipologia_id: int,
    payload: Tipologia_proyectoUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipologia_proyectoService(db, schema).updates(tipologia_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{tipologia_id}")
def delete(schema: str, 
    request: Request,
    tipologia_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipologia_proyectoService(db, schema).deletes(tipologia_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/{tipologia_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        tipologia_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipologia_proyectoService(db, schema).reactivate(tipologia_id, request, tokenpayload)
    return {"data": result}