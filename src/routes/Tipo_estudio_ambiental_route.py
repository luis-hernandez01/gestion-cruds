from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from src.config.config import (get_db)
from src.schemas.Tipo_estudio_ambiental_schema import (
    Tipo_estudio_ambientalCreate,
    PaginacionSchema,
    Tipo_estudio_ambientalUpdate,
)
from src.services.tipo_estudio_services import Tipo_estudioService
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
    return Tipo_estudioService(db, schema).all()
    

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
    data = Tipo_estudioService(db, schema).listar(activo=activo, filtros=filtros,
                                                            skip=skip, limit=limit)
    total = Tipo_estudioService(db, schema).count(activo=activo, filtros=filtros)
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
    payload: Tipo_estudio_ambientalCreate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipo_estudioService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{tipo_estudio_id}")
def get_show(schema: str, tipo_estudio_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return Tipo_estudioService(db, schema).show(tipo_estudio_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{tipo_estudio_id}")
def update(schema: str, 
    request: Request,
    tipo_estudio_id: int,
    payload: Tipo_estudio_ambientalUpdate,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipo_estudioService(db, schema).updates(tipo_estudio_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{tipo_estudio_id}")
def delete(schema: str, 
    request: Request,
    tipo_estudio_id: int,
    # de esta manera llamo todas las bases de datos existentes
    db: list[Session] = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    result = Tipo_estudioService(db, schema).deletes(tipo_estudio_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/{tipo_estudio_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        tipo_estudio_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Tipo_estudioService(db, schema).reactivate(tipo_estudio_id, request, tokenpayload)
    return {"data": result}