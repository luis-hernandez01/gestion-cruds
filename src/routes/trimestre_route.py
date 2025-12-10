from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.trimestre_services import TrimestreService
from src.schemas.trimestre_schema import (PaginacionSchema, 
                                                TrimestreCreate,
                                                TrimestreUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

@router.get("/{schema}/trimestre/all")
def list_all(schema: Optional[str],  request: Request,
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    schema = request.state.schema
    return TrimestreService(db, schema).all()




# endpoint de listar data con paginacion incluida
@router.get("/{schema}/trimestre/", response_model=PaginacionSchema)
def lista(schema: Optional[str],  request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo (true o false)"),
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    schema = request.state.schema
    skip = (page - 1) * per_page
    limit = per_page
    data = TrimestreService(db, schema).listar(activo=activo, skip=skip, limit=limit)
    total = TrimestreService(db, schema).count(activo=activo)  
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
@router.post("/{schema}/trimestre/")
def creates(schema: Optional[str], request: Request, 
                        payload: TrimestreCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = TrimestreService(db, schema).create(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/trimestre/{trimestre_id}")
def get_show(schema: Optional[str], request: Request, trimestre_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    return TrimestreService(db, schema).show(trimestre_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/trimestre/{trimestre_id}")
def update(schema: Optional[str], request: Request, 
                        trimestre_id: int,
                        payload: TrimestreUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = TrimestreService(db, schema).updates( trimestre_id, payload, request, tokenpayload)
    return {"data": result}


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/trimestre/{trimestre_id}")
def delete(schema: Optional[str], request: Request, 
                        trimestre_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = TrimestreService(db, schema).delete_modo(trimestre_id, request, tokenpayload)
    return {"data": result}



@router.post("/{schema}/trimestre/{trimestre_id}/reactivate")
def reactivates(schema: Optional[str], request: Request, 
                        trimestre_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    schema = request.state.schema
    result = TrimestreService(db, schema).reactivate(trimestre_id, request, tokenpayload)
    return {"data": result}