from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import (get_db)
from src.services.TipoClasificacionModos_services import TipoClasificacionModosService
from src.schemas.TipoClasificacionModos_schema import (PaginacionSchema, 
                                                TipoClasificacionModosCreate,
                                                TipoClasificacionModosUpdate)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()


@router.get("/{schema}/all")
def list_all(schema: str, 
    # de esta manera llamo solamente la primera base de datos
    id_modo: int,
    db: Session = Depends(get_db),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    return TipoClasificacionModosService(db, schema).all(id_modo)



# endpoint de listar data con paginacion incluida
@router.get("/{schema}/", response_model=PaginacionSchema)
def listar(schema: str, 
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
    data = TipoClasificacionModosService(db, schema).list_tipo_clasificacion(activo=activo, filtros=filtros, skip=skip, limit=limit)
    total = TipoClasificacionModosService(db, schema).count_tipo_clasificacion(activo=activo, filtros=filtros)  
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
def create(schema: str, request: Request, 
                        payload: TipoClasificacionModosCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)
                        ):
    result = TipoClasificacionModosService(db, schema).create_tipo_clasificacion(payload, request, tokenpayload)
    return {"data": result}


# endpoint de show o ver registro
@router.get("/{schema}/{tipo_clasificacion_id}")
def get_show(schema: str, tipo_clasificacion_id: int, 
                db: Session = Depends(get_db),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return TipoClasificacionModosService(db, schema).show(tipo_clasificacion_id)


# endpoin para actualizar un registro x
@router.put("/{schema}/{tipo_clasificacion_id}")
def update_unidades(schema: str, request: Request, 
                        tipo_clasificacion_id: int,
                        payload: TipoClasificacionModosUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(db, schema).update_tipo_clasificacion(tipo_clasificacion_id, payload, request, tokenpayload)
    return {"data": result}
    


# endpoint para eliminar un registro logicamente
@router.delete("/{schema}/{tipo_clasificacion_id}")
def delete(schema: str, request: Request, 
                        tipo_clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(db, schema).delete_tipo_clasificacion(tipo_clasificacion_id, request, tokenpayload)
    return {"data": result}


@router.post("/{schema}/{tipo_clasificacion_id}/reactivate")
def reactivates(schema: str, request: Request, 
                        tipo_clasificacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        db: list[Session] = Depends(get_db),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    result = TipoClasificacionModosService(db, schema).reactivate(tipo_clasificacion_id, request, tokenpayload)
    return {"data": result}