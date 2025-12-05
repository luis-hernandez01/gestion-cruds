from sqlalchemy import Column, Integer, Numeric, TIMESTAMP, Boolean, ForeignKey
from src.config.config import Base
from sqlalchemy.orm import relationship


def crear_modelo_Medidas_emisiones(base):
    """
    Crea dinámicamente la tabla 'actividades'
    para el schema asociado a la Base recibida.
    """
    class Medidas_emisiones(base):
        __tablename__ = "medidas_emisiones"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        valores = Column(Numeric(20, 14), nullable=False)
        id_tipomedida = Column(Integer, ForeignKey("tipo_medidas.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        
        
        tipomedida = relationship("Tipo_medidad", backref="medidas_emisiones")
        
        
        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Medidas_emisiones.__name__ = f"Medidas_emisiones_{base.metadata.schema}"
    return Medidas_emisiones


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Medidas_emisionesAika = crear_modelo_Medidas_emisiones(Base[0])
Medidas_emisionesWayra = crear_modelo_Medidas_emisiones(Base[1])
