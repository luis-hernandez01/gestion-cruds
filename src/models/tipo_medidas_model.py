from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_Tipo_medidad(base):
    """
    Crea dinámicamente la tabla 'actividades'
    para el schema asociado a la Base recibida.
    """
    class Tipo_medidad(base):
        __tablename__ = "tipo_medidas"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del tipo de proyecto")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Tipo_medidad.__name__ = f"Tipo_medidad_{base.metadata.schema}"
    return Tipo_medidad


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Tipo_medidadAika = crear_modelo_Tipo_medidad(Base[0])
Tipo_medidadWayra = crear_modelo_Tipo_medidad(Base[1])
