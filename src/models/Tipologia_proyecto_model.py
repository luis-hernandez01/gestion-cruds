from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_tipologia_proyecto(base):
    """
    Crea dinámicamente la tabla 'unidades de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Tipologia_proyecto(base):
        __tablename__ = "tipologia_proyecto"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Tipologia_proyecto.__name__ = f"Tipologia_proyecto_{base.metadata.schema}"
    return Tipologia_proyecto


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Tipologia_proyectoAika = crear_modelo_tipologia_proyecto(Base[0])
Tipologia_proyectoWayra = crear_modelo_tipologia_proyecto(Base[1])


