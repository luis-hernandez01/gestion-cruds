from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.logs_model import TipoOperacionEnum
from src.schemas.proyecto_schema import proyectoCreate, ProyectoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import LogUtil
from sqlalchemy import asc
from src.config.dinamic_tables import get_Proyecto_table

# Servicio para listar las unidades de ejecucion
class ProyectoService:
    def __init__(self, db: Session, schema: str):
        self.db = db
        self.schema = schema
        self.table = get_Proyecto_table(schema)
        
    
    def all(self):
        return (
            self.db.query(self.table)
            .filter(self.table.activo == True)
            .order_by(asc(self.table.nombre_unidades))
            .all()
        )
    
        
# servicio para listar  los registros
    def list_proyecto(self, skip: int, limit: int, filtros: str | None = None,
                            activo: bool | None = None):
        query = self.db.query(self.table)
        if activo is not None:
            query = query.filter(self.table.activo == activo)
        
        if filtros:
            query = query.filter(self.table.id.ilike(f"%{filtros}%"))
        
        return ( query.order_by(asc(self.table.id))
                .offset(skip)
                .limit(limit)
                .all()
                )
        
    def count_proyecto(self, activo: bool | None = None, filtros: str | None = None):
        query = self.db.query(self.table)

        if activo is not None:
            query = query.filter(self.table.activo == activo)

        if filtros:
            query = query.filter(self.table.id.ilike(f"%{filtros}%"))

        return query.count()
    
    
    # servicio para crear un registro
    def create_proyecto(self, payload: proyectoCreate, 
                            request: Request, tokenpayload: dict):
        
        data = payload.model_dump()
        
        try:
            for key in [
                "id_unidad_ejecutora",
                "id_direccion_territorial",
                "id_tipo_proyecto",
                "id_ruta",
                "id_tramo_sector",
                "id_clasificacion",
                "id_modo_transporte",
                "id_tipoclasificacion_modo",
                "catalogo",
            ]:
                if data.get(key) == 0:
                    data[key] = None
                    
            data["activo"] = True
            data["id_persona"] = tokenpayload.get("sub")
            data["created_at"] = datetime.utcnow()
            entity = self.table(**data)
            
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error insertando: {e}")
        
        # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="proyecto",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(entity)
    
    
    
    def show(self, proyecto_id: int):
        entity = self.db.query(self.table).filter(
            self.table.id == proyecto_id,
                self.table.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        if proyecto_id =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo proyecto_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    def update_proyecto(self, proyecto_id: int, 
                            payload: ProyectoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(self.table).filter(
            self.table.id == proyecto_id,
                self.table.activo == True).first()
        
        if not dataupdate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
            
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        
        try:
            dataupdate = (
                self.db.query(self.table)
                .filter(self.table.id == proyecto_id, self.table.activo == True)
                .first()
            )
            if dataupdate:
                for field, value in payload.model_dump(exclude_unset=True).items():
                    # 🔍 Convierte automáticamente valores 0 en None para claves foráneas
                    if field in [
                        "id_unidad_ejecutora",
                        "id_direccion_territorial",
                        "id_tipo_proyecto",
                        "id_ruta",
                        "id_tramo_sector",
                        "id_clasificacion",
                        "id_modo_transporte",
                        "id_tipoclasificacion_modo",
                        "catalogo",
                    ] and value == 0:
                        value = None

                    setattr(dataupdate, field, value)

                #  Campos de auditoría
                dataupdate.id_persona = tokenpayload.get("sub")
                dataupdate.updated_at = datetime.utcnow()

                self.db.commit()
                self.db.refresh(dataupdate)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando: {e}")
            
            # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="proyecto",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    def delete_proyecto(self, proyecto_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(self.table).filter(
            self.table.id == proyecto_id,
                self.table.activo == True).first()
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El proyecto no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        
        try:
            datadelete = self.db.query(self.table).filter(self.table.id == proyecto_id, self.table.activo == True).first()
            if not datadelete:
                return {"detail": "Registro no encontrado"}
        # le paso un valor false para realizar un sofdelete para un eliminado logico
            datadelete.activo = False
            datadelete.deleted_at = datetime.utcnow()
            datadelete.id_persona = tokenpayload.get("sub")
            # guardar los cambios
            self.db.commit()
            self.db.refresh(datadelete)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando: {e}")
        
        
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="proyecto",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(datadelete)
    
    
    # servicio para reactivar logicamente un registro
    def reactivate(self, proyecto_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db.query(self.table).filter(
            self.table.id == proyecto_id).first()
        if not datareactivate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        
        try:
            
            datareactivate = self.db.query(self.table).filter(self.table.id == proyecto_id).first()
            if not datareactivate:
                return {"detail": "Registro no encontrado"}
        # le paso un valor false para realizar un sofdelete para un eliminado logico
            datareactivate.activo = True
            datareactivate.deleted_at = datetime.utcnow()
            datareactivate.id_persona = tokenpayload.get("sub")
            # guardar los cambios
            self.db.commit()
            self.db.refresh(datareactivate)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando : {e}")
        
        
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="proyectos",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(datareactivate)