from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
from src.services.processor import process_all
from src.schemas.calculo_excel_schema import Emision4Item, EmisionTrimestreItem
from typing import List, Optional
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

# default_trimestre = [
#     {"ID": "90" ,"Trimestral": "Trimestral 1", "Emisiones": 1, "Tramo":"Transversal el Libertador"}
# ]

@router.post("/{schema}/procesar")
async def procesar_json(
    emisiones4: List[Emision4Item],
    emisiones_trimestre: List[EmisionTrimestreItem]
    
    # por si viene vacio
    # emisiones_trimestre: Optional[List[EmisionTrimestreItem]] = default_trimestre
):
    try:
        # -----------------------------
        # Convertir a DataFrame
        # -----------------------------
        df1 = pd.DataFrame([item.model_dump() for item in emisiones4])
        df2 = pd.DataFrame([item.model_dump() for item in emisiones_trimestre])
        
        # df2 = pd.DataFrame([EmisionTrimestreItem(**item).model_dump() for item in (emisiones_trimestre or [])])

        # -----------------------------
        # Validación de columnas
        # -----------------------------
        required_cols_1 = {"PR_INICIAL", "PR_FINAL", "Trimestral", "codigo_via"}
        required_cols_2 = {"Trimestral", "Emisiones"}

        if not required_cols_1.issubset(df1.columns):
            missing = required_cols_1 - set(df1.columns)
            raise HTTPException(status_code=400, detail=f"Faltan columnas en emisiones4 JSON: {missing}")

        if not required_cols_2.issubset(df2.columns):
            missing = required_cols_2 - set(df2.columns)
            raise HTTPException(status_code=400, detail=f"Faltan columnas en emisiones_trimestre JSON: {missing}")

        # -----------------------------
        # Procesar
        # -----------------------------
        result, short_result = process_all(df1, df2)

        # -----------------------------
        # Guardar archivos de salida
        # -----------------------------
        result_path = OUTPUT_DIR / "result.csv"
        short_path = OUTPUT_DIR / "short_result.csv"

        result.to_csv(result_path, index=False)
        short_result.to_csv(short_path, sep=';', decimal=',', index=False)

        # -----------------------------
        # Respuesta
        # -----------------------------
        return {
            "message": "Procesamiento completado",
            "download_result": "/download/result",
            "download_short": "/download/short",
            "rows_result": len(result),
            "rows_short": len(short_result)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/{schema}/download/result")
def download_result():
    path = OUTPUT_DIR / "result.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo result.csv no encontrado. Ejecuta /procesar primero.")
    return FileResponse(path, filename="result.csv")


@router.get("/{schema}/download/short")
def download_short():
    path = OUTPUT_DIR / "short_result.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo short_result.csv no encontrado. Ejecuta /procesar primero.")
    return FileResponse(path, filename="short_result.csv")