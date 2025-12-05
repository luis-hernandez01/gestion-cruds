from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.categoria_fuentesfijas_services import Categoria_fuentesfijas_Service
from src.schemas.Categoria_fuentefija_schema import (PaginacionSchema, 
                                                Categoria_fCreate,
                                                Categoria_fUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/all")
def list_all(schema: str, 
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return Categoria_fuentesfijas_Service(db, schema).all()


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
    data = Categoria_fuentesfijas_Service(db, schema).listar(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = Categoria_fuentesfijas_Service(db, schema).count(activo=activo, filtros=filtros)  
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
                        payload: Categoria_fCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{categoria_id}")
def get_show(schema: str, categoria_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return Categoria_fuentesfijas_Service(db, schema).show(categoria_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{categoria_id}")
def update(schema: str, request: Request, 
                        categoria_id: int,
                        payload: Categoria_fUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(db, schema).updates(categoria_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{categoria_id}")
def delete(schema: str, request: Request, 
                        categoria_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(db, schema).deletes(categoria_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/{categoria_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        categoria_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = Categoria_fuentesfijas_Service(db, schema).reactivate(categoria_id, request, tokenpayload)
    return {"data": result}