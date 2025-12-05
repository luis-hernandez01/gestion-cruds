from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from src.config.config import Base
from sqlalchemy.orm import relationship


def crear_modelo_Equipoproceso(base):
    """
    Crea dinámicamente la tabla 'presenta'
    para el schema asociado a la Base recibida.
    """
    class Equipoproceso(base):
        __tablename__ = "equipo_proceso"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        nombre = Column(String(255), unique=True, nullable=False, comment="Nombre del registro")
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        id_tipo_fuente = Column(Integer, ForeignKey("tipo_fuente.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        
        # Relaciones
        tipo_fuente = relationship("Tipofuente", backref="equipo_proceso")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Equipoproceso.__name__ = f"Tipofuente_{base.metadata.schema}"
    return Equipoproceso


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
EquipoprocesoAika = crear_modelo_Equipoproceso(Base[0])
EquipoprocesoWayra = crear_modelo_Equipoproceso(Base[1])
