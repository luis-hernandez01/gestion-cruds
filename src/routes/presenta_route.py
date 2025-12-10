from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.presenta_services import PresentaService
from src.schemas.Presenta_schema import (PaginacionSchema, 
                                                PresentaCreate,
                                                PresentaUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/presenta/all")
def list_all(schema: Optional[str],  request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return PresentaService(db, schema).all()


# endpoint de listar data con paginacion incluida
@router.get("/{schema}/presenta/", response_model=PaginacionSchema)
def lista(schema: Optional[str],  request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    schema = request.state.schema
    skip = (page - 1) * per_page
    limit = per_page
    data = PresentaService(db, schema).listar(activo=activo, skip=skip, limit=limit)
    total = PresentaService(db, schema).count(activo=activo)  
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
@router.post("/{schema}/presenta/")
def creates(schema: Optional[str], request: Request, 
                        payload: PresentaCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = PresentaService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/presenta/{presenta_id}")
def get_show(schema: Optional[str], request: Request, presenta_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return PresentaService(db, schema).show(presenta_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/presenta/{presenta_id}")
def update(schema: Optional[str], request: Request, 
                        presenta_id: int,
                        payload: PresentaUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = PresentaService(db, schema).updates(presenta_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/presenta/{presenta_id}")
def delete(schema: Optional[str], request: Request, 
                        presenta_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = PresentaService(db, schema).deletes(presenta_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/presenta/{presenta_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        presenta_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = PresentaService(db, schema).reactivate(presenta_id, request, tokenpayload)
    return {"data": result}