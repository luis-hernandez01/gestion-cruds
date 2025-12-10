# dependencias usadas para este archivo raiz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from src.config.config import Base, engine, DEBUG, HIDE_TES

# directorios de rutas
from src.routes import (
    TipoClasificacionModos_route,
    catalogo_route,
    clasificaciones_proyecto_route,
    departamento_route,
    direccion_territorial_route,
    modo_route,
    municipio_route,
    profesion_route,
    rutas_viales_route,
    tipos_proyectos_route,
    tramo_route,
    unidad_ejecutora_route,
    migrador_route,
    proyecto_route,
    contratos_route,
    polygon,
    line,
    point,
    trimestre_route,
    presenta_route,
    Unidades_factores_emision_route,
    Combustibles_emisiones_route,
    Categoria_emisiones_route,
    Categoria_fuentefija_route,
    Alcance_fuentefija_rouete,
    informe_route,
    calculos_excel_route,
    actividades_route,
    informe_via_link_route,
    calculos_excel_prueba,
    Tipofuente_route,
    Equipoproceso_route,
    factor_emisiones_route,
    medidas_emisiones_route,
    tipo_medidas_route,
    
    Actos_administrativos_route,
    Ciclo_vida_route,
    Tipo_contrato_route,
    Tipologia_proyecto_route,
    Tipo_estudio_ambiental_route,
    Periosidad_informe_route
)

from src.config.middleware import SchemaMiddleware


# # --- Crear tablas en todas las bases parametrizadas ---

# for base, eng in zip(Base, engine):
#     print(f"🛠️ Creando tablas en schema: {base.metadata.schema}")
#     base.metadata.create_all(bind=eng)


# Inicialización de la aplicación FastAPI
app = FastAPI(title="Servicios parametrizables", version="1.0.0",
            docs_url="/docs",           # Swagger
            redoc_url="/redoc",         # Redoc
    )

app.add_middleware(SchemaMiddleware)

    
# configuracion de CORS
# permite que aplicaciones externas (por ejemplo,
# un frontend en Angular o React)
# puedan comunicarse con esta API.
# CORS: ajusta a tus orígenes reales

allow_origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,           # ⚠️ Permitir todos los orígenes (solo para desarrollo)
    allow_credentials=True,        # Permitir envío de cookies/autenticación
    allow_methods=["*"],           # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Permitir todos los encabezados personalizados
)

# registrando mis rutas existentes de las difrentes APIs
# Aquí se incluyen las rutas definidas en la carpeta 'routes'.

app.include_router(Periosidad_informe_route.router, prefix="", tags=["Periosidad"])
app.include_router(Actos_administrativos_route.router, prefix="", tags=["Actos administrativos"])
app.include_router(Tipo_estudio_ambiental_route.router, prefix="", tags=["Tipo estudio ambiental"])
app.include_router(Tipologia_proyecto_route.router, prefix="", tags=["Ttipologia proyecto"])
app.include_router(Ciclo_vida_route.router, prefix="", tags=["Ciclo de vida"])
app.include_router(Tipo_contrato_route.router, prefix="", tags=["Tipo contrato"])




app.include_router(migrador_route.router, prefix="/migrar", tags=["Migrar"])

app.include_router(medidas_emisiones_route.router, prefix="", tags=["Medida"])
app.include_router(tipo_medidas_route.router, prefix="", tags=["tipo de medidas"])

app.include_router(factor_emisiones_route.router, prefix="", tags=["factores emisiones"])

app.include_router(Tipofuente_route.router, prefix="", tags=["Tipo fuentes"])
app.include_router(Equipoproceso_route.router, prefix="", tags=["Equipo proceso"])

app.include_router(actividades_route.router, prefix="", tags=["Actividades"])

app.include_router(informe_route.router, prefix="/informes", tags=["Informes"])
app.include_router(informe_via_link_route.router, prefix="/informes_via_link", tags=["Informes via link"])
app.include_router(calculos_excel_route.router, prefix="/calculos", tags=["calculos excel"])

app.include_router(calculos_excel_prueba.router, prefix="/calculos_pueba", tags=["calculos excel pueba"])

app.include_router(Categoria_fuentefija_route.router, prefix="", tags=["Categoria fuentes fijas"])
app.include_router(Alcance_fuentefija_rouete.router, prefix="", tags=["Alcance fuentes fijas"])

app.include_router(Combustibles_emisiones_route.router, prefix="", tags=["Combutibles"])
app.include_router(Categoria_emisiones_route.router, prefix="", tags=["Categoria vehiculo"])
app.include_router(Unidades_factores_emision_route.router, prefix="", tags=["Unidades de los factores de emisión"])


app.include_router(trimestre_route.router, prefix="", tags=["Trimestre"])
app.include_router(presenta_route.router, prefix="", tags=["Presenta"])

app.include_router(
    municipio_route.router,
    prefix="",
    tags=["Municipios"],
)

app.include_router(
    departamento_route.router,
    prefix="",
    tags=["Departamentos"],
)

app.include_router(
    profesion_route.router,
    prefix="",
    tags=["Profesion"],
)

app.include_router(
    direccion_territorial_route.router,
    prefix="",
    tags=["Direccion territorial"],
)
app.include_router(
    tipos_proyectos_route.router, prefix="", tags=["Tipos de proyectos"]
)

app.include_router(tramo_route.router, prefix="", tags=["Tramos"])

app.include_router(
    rutas_viales_route.router, prefix="", tags=["Rutas viales"]
)

app.include_router(
    unidad_ejecutora_route.router, prefix="", tags=["Unidad ejecutora"]
)
app.include_router(
    clasificaciones_proyecto_route.router,
    prefix="",
    tags=["Clasificacion proyectos"],
)
app.include_router(
    TipoClasificacionModos_route.router,
    prefix="",
    tags=["Tipo clasifificacion de modos"],
)
app.include_router(modo_route.router, prefix="", tags=["Modo"])

app.include_router(
    catalogo_route.router, prefix="", 
    tags=["Catalogo de modos por tipo clasificacion"]
)

app.include_router(
    proyecto_route.router,
    prefix="",
    tags=["Proyecto"],
)

app.include_router(
    contratos_route.router,
    prefix="",
    tags=["Contratos"],
)

app.include_router(polygon.router, prefix="")
app.include_router(line.router, prefix="")
app.include_router(point.router, prefix="")


#  Documentación con Swagger/OpenAPI

# if HIDE_TES == "development":
app.mount("/scalar", get_scalar_api_reference())


# para render por el puerto 10000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=10000, 
                reload=DEBUG)
