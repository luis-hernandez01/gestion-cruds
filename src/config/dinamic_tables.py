from src.models.actividades_model import actividadesAika, actividadesWayra
def get_actividades_table(schema: str):
    if schema == "Aika":
        return actividadesAika
    if schema == "wayra":
        return actividadesWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.logs_model import LogsAika, LogsWayra
def get_logs_table(schema: str):
    if schema == "Aika":
        return LogsAika
    if schema == "wayra":
        return LogsWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.Actos_administrativos_model import (Actos_administrativosAika, Actos_administrativosWayra)
def get_Actos_administrativos_table(schema: str):
    if schema == "Aika":
        return Actos_administrativosAika
    if schema == "wayra":
        return Actos_administrativosWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Alcance_fuentefija_model import (Alcance_fuentefijaAika, Alcance_fuentefijaWayra)
def get_Alcance_fuentefija_table(schema: str):
    if schema == "Aika":
        return Alcance_fuentefijaAika
    if schema == "wayra":
        return Alcance_fuentefijaWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.catalogomodoXtipoclasificacion_model import (
    CatalogoModoXTipoClasificacionAika, CatalogoModoXTipoClasificacionWayra)
def get_catalogomodoXtipoclasificacion_table(schema: str):
    if schema == "Aika":
        return CatalogoModoXTipoClasificacionAika
    if schema == "wayra":
        return CatalogoModoXTipoClasificacionWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.categoria_emisiones_model import (Categoria_emisionesAika, Categoria_emisionesnWayra)
def get_categoria_emisiones_table(schema: str):
    if schema == "Aika":
        return Categoria_emisionesAika
    if schema == "wayra":
        return Categoria_emisionesnWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Categoria_fuentefija_model import (Categoria_fuentefijaAika, Categoria_fuentefijaWayra)
def get_Categoria_fuentefija_table(schema: str):
    if schema == "Aika":
        return Categoria_fuentefijaAika
    if schema == "wayra":
        return Categoria_fuentefijaWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.Ciclo_vida_model import (Ciclo_vidaAika, Ciclo_vidaWayra)
def get_Ciclo_vida_table(schema: str):
    if schema == "Aika":
        return Ciclo_vidaAika
    if schema == "wayra":
        return Ciclo_vidaWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.clasificaciones_proyecto_model import (ClasificacionesProyectoAika, ClasificacionesProyectoWayra)
def get_clasificaciones_proyecto_table(schema: str):
    if schema == "Aika":
        return ClasificacionesProyectoAika
    if schema == "wayra":
        return ClasificacionesProyectoWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.combustible_emisiones_model import (Combustibles_emisionesAika, Combustibles_emisionesWayra)
def get_combustible_emisiones_table(schema: str):
    if schema == "Aika":
        return Combustibles_emisionesAika
    if schema == "wayra":
        return Combustibles_emisionesWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.contratos_model import (ContratoAika, ContratoWayra)
def get_contratos_table(schema: str):
    if schema == "Aika":
        return ContratoAika
    if schema == "wayra":
        return ContratoWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.divipola import (DepartamentoAika, DepartamentoWayra)
def get_divipola_depar_table(schema: str):
    if schema == "Aika":
        return DepartamentoAika
    if schema == "wayra":
        return DepartamentoWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.direcciones_territoriales_model import (DireccionesTerritorialesAika, DireccionesTerritorialesWayra)
def get_direcciones_territoriales_table(schema: str):
    if schema == "Aika":
        return DireccionesTerritorialesAika
    if schema == "wayra":
        return DireccionesTerritorialesWayra
    
    raise ValueError(f"Schema '{schema}' no válido")



from src.models.Equipoproceso_model import (EquipoprocesoAika, EquipoprocesoWayra)
def get_Equipoproceso_table(schema: str):
    if schema == "Aika":
        return EquipoprocesoAika
    if schema == "wayra":
        return EquipoprocesoWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.factores_emision_model import (Factores_emisionAika, Factores_emisionWayra)
def get_factores_emision_table(schema: str):
    if schema == "Aika":
        return Factores_emisionAika
    if schema == "wayra":
        return Factores_emisionWayra
    
    raise ValueError(f"Schema '{schema}' no válido")


# from src.models.divipola import DepartamentoAika as Departamento, MunicipioAika as Municipio
# def get_line_table(schema: str):
#     if schema == "Aika":
#         return Departamento
#     if schema == "wayra":
#         return Factores_emisionWayra
    
#     raise ValueError(f"Schema '{schema}' no válido")


from src.models.medidas_emisiones_model import (Medidas_emisionesAika, Medidas_emisionesWayra)
def get_medidas_emisiones_table(schema: str):
    if schema == "Aika":
        return Medidas_emisionesAika
    if schema == "wayra":
        return Medidas_emisionesWayra
    
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.modo_model import (ModoAika, ModoWayra)
def get_modo_table(schema: str):
    if schema == "Aika":
        return ModoAika
    if schema == "wayra":
        return ModoWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.divipola import (MunicipioAika, MunicipioWayra)
def get_municipio_table(schema: str):
    if schema == "Aika":
        return MunicipioAika
    if schema == "wayra":
        return MunicipioWayra
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.Periosidad_informe_model import (Periosidad_informeAika, Periosidad_informeWayra)
def get_Periosidad_informe_table(schema: str):
    if schema == "Aika":
        return Periosidad_informeAika
    if schema == "wayra":
        return Periosidad_informeWayra
    raise ValueError(f"Schema '{schema}' no válido")

# from src.models.divipola import DepartamentoAika, MunicipioAika
# def get_pointer_table(schema: str):
#     if schema == "Aika":
#         return Periosidad_informeAika
#     if schema == "wayra":
#         return Periosidad_informeWayra
#     raise ValueError(f"Schema '{schema}' no válido")


# from src.models.divipola import DepartamentoAika, MunicipioAika
# def get_polygon_table(schema: str):
#     if schema == "Aika":
#         return Periosidad_informeAika
#     if schema == "wayra":
#         return Periosidad_informeWayra
#     raise ValueError(f"Schema '{schema}' no válido")

from src.models.Presenta_model import (PresentaAika, PresentaWayra)
def get_Presenta_table(schema: str):
    if schema == "Aika":
        return PresentaAika
    if schema == "wayra":
        return PresentaWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.profesion_model import (ProfesionAika, ProfesionWayra)
def get_profesion_table(schema: str):
    if schema == "Aika":
        return ProfesionAika
    if schema == "wayra":
        return ProfesionWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Proyecto_model import (ProyectoAika, ProyectoWayra)
def get_Proyecto_table(schema: str):
    if schema == "Aika":
        return ProyectoAika
    if schema == "wayra":
        return ProyectoWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.rutas_viales_model import (RutasVialesAika, RutasVialesWayra)
def get_rutas_viales_table(schema: str):
    if schema == "Aika":
        return RutasVialesAika
    if schema == "wayra":
        return RutasVialesWayra
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.Tipo_contrato_model import (Tipo_contratoAika, Tipo_contratoWayra)
def get_Tipo_contrato_table(schema: str):
    if schema == "Aika":
        return Tipo_contratoAika
    if schema == "wayra":
        return Tipo_contratoWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Tipo_estudio_ambiental_model import (Tipo_estudio_ambientalAika, Tipo_estudio_ambientalWayra)
def get_Tipo_estudio_ambiental_table(schema: str):
    if schema == "Aika":
        return Tipo_estudio_ambientalAika
    if schema == "wayra":
        return Tipo_estudio_ambientalWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Tipofuente_model import (TipofuenteAika, TipofuenteWayra)
def get_Tipofuente_table(schema: str):
    if schema == "Aika":
        return TipofuenteAika
    if schema == "wayra":
        return TipofuenteWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.tipo_medidas_model import (Tipo_medidadAika, Tipo_medidadWayra)
def get_tipo_medidas_table(schema: str):
    if schema == "Aika":
        return Tipo_medidadAika
    if schema == "wayra":
        return Tipo_medidadWayra
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.TipoClasificacionModos_model import (TipoClasificacionModosAika, TipoClasificacionModosWayra)
def get_TipoClasificacionModos_table(schema: str):
    if schema == "Aika":
        return TipoClasificacionModosAika
    if schema == "wayra":
        return TipoClasificacionModosWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.Tipologia_proyecto_model import (Tipologia_proyectoAika, Tipologia_proyectoWayra)
def get_Tipologia_proyecto_table(schema: str):
    if schema == "Aika":
        return Tipologia_proyectoAika
    if schema == "wayra":
        return Tipologia_proyectoWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.tipos_proyecto_model import (TiposProyectoAika, TiposProyectoWayra)
def get_tipos_proyecto_table(schema: str):
    if schema == "Aika":
        return TiposProyectoAika
    if schema == "wayra":
        return TiposProyectoWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.tramos_sectores_model import (TramoSectoresAika, TramoSectoresWayra)
def get_tramos_sectores_table(schema: str):
    if schema == "Aika":
        return TramoSectoresAika
    if schema == "wayra":
        return TramoSectoresWayra
    raise ValueError(f"Schema '{schema}' no válido")


from src.models.Trimestre_model import (TrimestreAika, TrimestreWayra)
def get_Trimestre_table(schema: str):
    if schema == "Aika":
        return TrimestreAika
    if schema == "wayra":
        return TrimestreWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.unidad_ejecutora_model import (UnidadEjecutoraAika, UnidadEjecutoraWayra)
def get_unidad_ejecutora_table(schema: str):
    if schema == "Aika":
        return UnidadEjecutoraAika
    if schema == "wayra":
        return UnidadEjecutoraWayra
    raise ValueError(f"Schema '{schema}' no válido")

from src.models.unidades_factores_emision_model import (Unidades_factores_emisionAika, Unidades_factores_emisionWayra)
def get_unidades_factores_emision_table(schema: str):
    if schema == "Aika":
        return Unidades_factores_emisionAika
    if schema == "wayra":
        return Unidades_factores_emisionWayra
    raise ValueError(f"Schema '{schema}' no válido")