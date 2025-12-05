from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base


def crear_modelo_periosidad_informe(base):
    """
    Crea dinámicamente la tabla 'unidades de emisiones'
    para el schema asociado a la Base recibida.
    """
    class Periosidad_informe(base):
        __tablename__ = "periosidad_informe"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la profesión")
        nombre = Column(String(255), nullable=False)

        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Cambiar dinámicamente el nombre de la clase según el schema
    Periosidad_informe.__name__ = f"Periosidad_informe_{base.metadata.schema}"
    return Periosidad_informe


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Periosidad_informeAika = crear_modelo_periosidad_informe(Base[0])
Periosidad_informeWayra = crear_modelo_periosidad_informe(Base[1])


