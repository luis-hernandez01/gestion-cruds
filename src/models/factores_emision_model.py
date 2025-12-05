from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Numeric, ForeignKey
from src.config.config import Base
def crear_modelo_factores_emision(base):
    """
    Crea dinámicamente la tabla 'facores'
    para el schema asociado a la Base recibida.
    """
    class Factores_emision(base):
        __tablename__ = "factores_emision"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del registro")
        
        id_tipofuente = Column(Integer, ForeignKey("tipo_fuente.id", ondelete="NO ACTION"), nullable=True)

        id_equipoproceso = Column(Integer, ForeignKey("equipo_proceso.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
        id_categoria = Column(Integer, ForeignKey("categoria_emisiones.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
        id_Combustible = Column(Integer, ForeignKey("combustibles_emisiones.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)

        N2O_kg_gal = Column(Numeric(20, 14), nullable=True)
        CO2_kg_gal = Column(Numeric(20, 14), nullable=True)
        CH4_kg_km = Column(Numeric(20, 14), nullable=True)

        id_unidades_factor_emision = Column(Integer, ForeignKey("unidades_factores_emision.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
        
        
        
        id_persona = Column(Integer, nullable=True, comment="ID de la persona que creó o modificó el registro")
        activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")

        # Campos de auditoría
        created_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de creación del registro")
        updated_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de última actualización del registro")
        deleted_at = Column(TIMESTAMP, nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")

    # Renombrar clase según el schema
    Factores_emision.__name__ = f"Factores_emision_{base.metadata.schema}"
    return Factores_emision


# ==========================================================
# INSTANCIAS DE MODELOS POR SCHEMA
# ==========================================================
Factores_emisionAika = crear_modelo_factores_emision(Base[0])
Factores_emisionWayra = crear_modelo_factores_emision(Base[1])
