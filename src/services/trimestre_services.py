from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.logs_model import TipoOperacionEnum
from src.schemas.trimestre_schema import TrimestreCreate, TrimestreUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import LogUtil
from sqlalchemy import asc
from src.config.dinamic_tables import get_Trimestre_table

# Servicio para listar las unidades de ejecucion
class TrimestreService:
    def __init__(self, db: Session, schema: str):
        self.db = db
        self.schema = schema
        self.table = get_Trimestre_table(schema)
        
    def all(self):
        return (
            self.db.query(self.table)
            .filter(self.table.activo == True)
            .order_by(asc(self.table.nombre))
            .all()
        )
    
        
# servicio para listar  los registros
    def listar(self, skip: int, limit: int, activo: bool | None = None):
        return self.db.query(self.table).filter(self.table.activo == activo).order_by(asc(self.table.nombre)).offset(skip).limit(limit).all()
    def count(self, activo: bool | None = None):
        return self.db.query(self.table).filter(self.table.activo == activo).count()
    
    
    # servicio para crear un registro
    def create(self, payload: TrimestreCreate, 
                            request: Request, tokenpayload: dict):
        datacreate = self.db.query(self.table).filter(
            self.table.nombre == payload.nombre).first()
        if datacreate:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este registro ya se encuentra creado. Se requiere su reactivación.")
        if payload.nombre =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        
        
        try:
            entity = self.table(nombre=payload.nombre, id_persona=tokenpayload.get("sub"), 
                                            activo=True, created_at=datetime.utcnow())
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando: {e}")
                
        # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="trimestre",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(entity)
    
    
    
    def show(self, trimestre_id: int):
        entity = self.db.query(self.table).filter(
            self.table.id == trimestre_id,
                self.table.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if trimestre_id =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo trimestre_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    def updates(self, trimestre_id: int, 
                            payload: TrimestreUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(self.table).filter(
            self.table.id == trimestre_id,
                self.table.activo == True).first()
        if payload.nombre:
            existe = (
                self.db.query(self.table)
                .filter(self.table.nombre == payload.nombre, self.table.id != trimestre_id)
                .first()
            )
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro registro."
                )
        
        if not dataupdate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if payload.nombre =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
        
        
        try:
            registro = self.db.query(self.table).filter(self.table.id == trimestre_id, self.table.activo == True).first()
            if not registro:
                return {"detail": "Registro no encontrado"}
            
            if registro:
                registro.nombre = payload.nombre
                registro.id_persona = tokenpayload.get("sub")
                registro.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(registro)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando : {e}")
                    
            # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="trimestre",
            id_registro_afectado=registro.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(registro).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=registro.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(registro)
    
    
    # servicio para eliminar logicamente un registro
    def delete_modo(self, trimestre_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(self.table).filter(
            self.table.id == trimestre_id,
                self.table.activo == True).first()
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        
        
        try:
            registro = self.db.query(self.table).filter(self.table.id == trimestre_id, self.table.activo == True).first()
            if not registro:
                return {"detail": "Registro no encontrado"}
        # le paso un valor false para realizar un sofdelete para un eliminado logico
            registro.activo = False
            registro.deleted_at = datetime.utcnow()
            registro.id_persona = tokenpayload.get("sub")
            # guardar los cambios
            self.db.commit()
            self.db.refresh(registro)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando : {e}")
                
                
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="trimestre",
            id_registro_afectado=registro.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(registro).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=registro.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(registro)
    
    
    
    # servicio para reactivar logicamente un registro
    def reactivate(self, trimestre_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db.query(self.table).filter(
            self.table.id == trimestre_id).first()
        if not datareactivate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        
        try:
            
            registro = self.db.query(self.table).filter(self.table.id == trimestre_id).first()
            if not registro:
                return {"detail": "Registro no encontrado"}
            
            # le paso un valor false para realizar un sofdelete para un eliminado logico
            registro.activo = True
            registro.deleted_at = datetime.utcnow()
            registro.id_persona = tokenpayload.get("sub")
            # guardar los cambios
            self.db.commit()
            self.db.refresh(registro)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error insertando: {e}")
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="trimestre",
            id_registro_afectado=registro.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(registro).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=registro.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(registro)