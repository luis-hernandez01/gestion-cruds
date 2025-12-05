from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

# from src.models.modo_model import ModoAika
# from src.models.TipoClasificacionModos_model import TipoClasificacionModosAika

from src.models.logs_model import TipoOperacionEnum
from src.schemas.catalogomodoXtipoclasificacion_schema import CatalogoCreate, CatalogoUpdate, LogEntityRead
from datetime import datetime
from src.utils.logs_util import LogUtil
from sqlalchemy import asc, or_
from src.config.dinamic_tables import get_catalogomodoXtipoclasificacion_table
from src.config.dinamic_tables import get_modo_table
from src.config.dinamic_tables import get_TipoClasificacionModos_table

# Servicio para listar las unidades de ejecucion
class catalogoService:
    def __init__(self, db: Session, schema: str):
        self.db = db
        self.schema = schema
        self.table = get_catalogomodoXtipoclasificacion_table(schema)
        self.table2 = get_modo_table(schema)
        self.table3 = get_TipoClasificacionModos_table(schema)
        
    def all(self, id_modo, id_tipo):
        return (
            self.db.query(self.table)
            .filter(self.table.activo == True,
                    self.table.id_modo == id_modo,
                    self.table.id_tipo_clasificacion_modos == id_tipo)
            .order_by(asc(self.table.nombre))
            .all()
        )
    
        
# servicio para listar  los registros
    # def list_catalogo(self, skip: int, limit: int):
    #     return self.db.query(catalogomodoXtipoclasificacion).filter(catalogomodoXtipoclasificacion.activo == True).offset(skip).limit(limit).all()
    
    # def list_catalogo(self, skip: int, limit: int, activo: bool | None = None):
    #     data = (
    #         self.db.query(self.table)
    #         .join(self.table.modos)
    #         .join(self.table.tipoclasificacion)
    #         .order_by(asc(self.table.nombre))
    #         .filter(self.table.activo == activo)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    #     return [
    #         {
    #             "id": rw.id,
    #             "nombre": rw.nombre,
    #             "id_modo": rw.modos.id if rw.modos else None,
    #             "id_tipo_clasificacion_modos": rw.tipoclasificacion.id if rw.tipoclasificacion else None,
    #             "modos": rw.modos.nombre if rw.modos else None,
    #             "tipoclasificacion": rw.tipoclasificacion.nombre if rw.tipoclasificacion else None
    #         }
    #         for rw in data
    #     ]
    
    

    def list_catalogo(
        self,
        skip: int,
        limit: int,
        activo: bool | None = None,
        filtros: str | None = None
    ):
        query = (
            self.db.query(self.table)
            .join(self.table.modos)
            .join(self.table.tipoclasificacion)
            .order_by(asc(self.table.nombre))
        )

        # Filtro por activo (opcional)
        if activo is not None:
            query = query.filter(self.table.activo == activo)

        # FILTRO GENERAL (multi-campo)
        if filtros:
            filtros_like = f"%{filtros}%"
            query = query.filter(
                or_(
                    self.table.nombre.ilike(filtros_like),
                    self.table.modos.has(
                        self.table2.nombre.ilike(filtros_like)
                    ),
                    self.table.tipoclasificacion.has(
                        self.table3.nombre.ilike(filtros_like)
                    ),
                )
            )

        data = query.offset(skip).limit(limit).all()

        # Construcción del resultado final
        return [
            {
                "id": rw.id,
                "nombre": rw.nombre,
                "id_modo": rw.id_modo,
                "id_tipo_clasificacion_modos": rw.id_tipo_clasificacion_modos,
                "modos": rw.modos.nombre if rw.modos else None,
                "tipoclasificacion": rw.tipoclasificacion.nombre if rw.tipoclasificacion else None,
                "activo": rw.activo
            }
            for rw in data
        ]

    
    
    def count_catalogo(self, activo: bool | None = None, filtros: str | None = None):
        query = self.db.query(self.table)

        if activo is not None:
            query = query.filter(self.table.activo == activo)

        if filtros:
            query = query.filter(self.table.nombre.ilike(f"%{filtros}%"))

        return query.count()
    
    
    # servicio para crear un registro
    def create_catalogo(self, payload: CatalogoCreate, 
                            request: Request, tokenpayload: dict):
        
        
        if payload.nombre =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        
        if payload.id_modo =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo modo se encuentra vacia ingresa un dato valido")
        
        if payload.id_tipo_clasificacion_modos =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo tipo clasificacion se encuentra vacia ingresa un dato valido")
        
        if len(payload.nombre) > 255:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        
        
        try:
            entity = self.table(nombre=payload.nombre, 
                            id_modo=payload.id_modo,
                            id_tipo_clasificacion_modos=payload.id_tipo_clasificacion_modos,
                            id_persona=tokenpayload.get("sub"), 
                            activo=True, created_at=datetime.utcnow())
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando: {e}")
        
        # # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(entity)
    
    
    
    def show(self, catalogo_id: int):
        entity = self.db.query(self.table).filter(
            self.table.id == catalogo_id,
                self.table.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if catalogo_id =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo catalogo_id se encuentra vacia ingresa un dato valido")
        return entity
    
    # servicio para editar logicamente un registro
    def update_catalogo(self, catalogo_id: int, 
                            payload: CatalogoUpdate, 
                            request: Request, tokenpayload: dict):
        dataupdate = self.db.query(self.table).filter(
            self.table.id == catalogo_id,
                self.table.activo == True).first()
        
        if not dataupdate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if payload.nombre =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre se encuentra vacia ingresa un dato valido")
        if payload.id_modo =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo modo se encuentra vacia ingresa un dato valido")
        
        if payload.id_tipo_clasificacion_modos =="":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo tipo clasificacion se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        datos_viejos = LogEntityRead.from_orm(dataupdate).model_dump(mode="json")
            
        
        try:
            dataupdate = (
                self.db.query(self.table)
                .filter(self.table.id == catalogo_id, self.table.activo == True)
                .first()
            )

            if dataupdate:
                dataupdate.nombre = payload.nombre
                dataupdate.id_persona = tokenpayload.get("sub")
                dataupdate.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(dataupdate)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Error insertando: {e}")
            
            # Registro de logs
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=dataupdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataupdate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=dataupdate.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(dataupdate)
    
    
    # servicio para eliminar logicamente un registro
    def delete_catalogo(self, catalogo_id: int, request: Request, tokenpayload: dict):
        datadelete = self.db.query(self.table).filter(
            self.table.id == catalogo_id,
                self.table.activo == True).first()
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")
        
        try:
            registro = self.db.query(self.table).filter(self.table.id == catalogo_id, self.table.activo == True).first()
            if not registro:
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
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(datadelete)
    
    
     # servicio para reactivar logicamente un registro
    def reactivate(self, catalogo_id: int, request: Request, tokenpayload: dict):
        datareactivate = self.db.query(self.table).filter(
            self.table.id == catalogo_id).first()
        if not datareactivate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        
        if datareactivate.activo:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        datos_viejos = LogEntityRead.from_orm(datareactivate).model_dump(mode="json")
        
        
        try:
            
            datareactivate = self.db.query(self.table).filter(self.table.id == catalogo_id).first()
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
                            detail=f"Error insertando: {e}")
        
        
        LogUtil(self.db, self.schema).registrar_log(
            tabla_afectada="catalogo_modoXtipo_clasificacion",
            id_registro_afectado=datareactivate.id,
            tipo_operacion=TipoOperacionEnum.REACTIVATE,
            datos_nuevos=LogEntityRead.from_orm(datareactivate).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datareactivate.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("User-Agent", "")[:255])
        
        return LogEntityRead.from_orm(datareactivate)
    
    