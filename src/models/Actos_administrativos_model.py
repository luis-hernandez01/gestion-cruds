from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_actos_administrativos(base):
    """
    Crea dinámicamente la tabla 'unidades de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Actos_administrativos(base):
        __tablename__ = "actos_administrativos"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Actos_administrativos.__name__ = f"Ciclo_vida_{base.metadata.schema}"
    return Actos_administrativos


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Actos_administrativosAika = crear_modelo_actos_administrativos(Base[0])
Actos_administrativosWayra = crear_modelo_actos_administrativos(Base[1])


