from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_actividades(base):
    """
    Crea dinámicamente la tabla 'actividades'
    para el schema asociado a la Base recibida.
    """
    class actividades(base):
        __tablename__ = "actividades"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), nullable=False, comment="Nombre del registro")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    actividades.__name__ = f"actividades_{base.metadata.schema}"
    return actividades


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
actividadesAika = crear_modelo_actividades(Base[0])
actividadesWayra = crear_modelo_actividades(Base[1])