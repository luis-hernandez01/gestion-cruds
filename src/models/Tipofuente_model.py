from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_tipo_fuente(base):
    """
    Crea dinámicamente la tabla 'presenta'
    para el schema asociado a la Base recibida.
    """
    class Tipofuente(base):
        __tablename__ = "tipo_fuente"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del registro")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Tipofuente.__name__ = f"Tipofuente_{base.metadata.schema}"
    return Tipofuente


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
TipofuenteAika = crear_modelo_tipo_fuente(Base[0])
TipofuenteWayra = crear_modelo_tipo_fuente(Base[1])
