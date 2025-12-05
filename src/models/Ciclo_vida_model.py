from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_ciclo_vida(base):
    """
    Crea dinámicamente la tabla 'unidades de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Ciclo_vida(base):
        __tablename__ = "ciclo_vida"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Ciclo_vida.__name__ = f"Ciclo_vida_{base.metadata.schema}"
    return Ciclo_vida


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Ciclo_vidaAika = crear_modelo_ciclo_vida(Base[0])
Ciclo_vidaWayra = crear_modelo_ciclo_vida(Base[1])


