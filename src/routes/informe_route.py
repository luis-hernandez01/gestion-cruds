from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from playwright.sync_api import sync_playwright
from starlette.concurrency import run_in_threadpool
import httpx
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter, Depends, Query, Request
from src.utils.jwt_validator_util import verify_jwt_token, others_verify_jwt_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

executor = ThreadPoolExecutor(max_workers=2)

# Playwright (PDF)
def generar_pdf_sync(html: str):
    buffer = BytesIO()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.set_content(html, wait_until="load")

        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            display_header_footer=True,
            margin={"top": "60px", "bottom": "60px", "left": "20px", "right": "20px"},
            header_template="""
                <div style="font-size:10px; width:100%; text-align:center; margin-top:10px;">
                    <span class="date"></span> — <span class="title"></span>
                </div>
            """,
            footer_template="""
                <div style="font-size:10px; width:100%; text-align:center; margin-bottom:10px;">
                    Página <span class="pageNumber"></span> de <span class="totalPages"></span>
                </div>
            """
        )

        buffer.write(pdf_bytes)
        buffer.seek(0)
        browser.close()

    return buffer


# -----------------------------
# 🔵 NUEVO ENDPOINT
# Consume el API externo y genera PDF
# -----------------------------
@router.get("/contract-to-pdf/{contract_code}")
async def contract_to_pdf(
    contract_code: str,
    tokenpayload: dict = Depends(others_verify_jwt_token) ):
    
    try:
        token = tokenpayload["token"]            # "Bearer <token>"
    except:
        # raise HTTPException(status_code=400, detail="Formato de token inválido")
        return {"error": "Formato de token inválido"}
    

    external_url = (
        "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/form/by-contract-code"
    )
    url_emisiones = "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/api/v1/emissions"
    
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/html"
    }
    
    # Llamada al servicio externo
    async with httpx.AsyncClient() as client:
        # Servicio 1: Contrato
        resp = await client.get(
            external_url,
            params={"contract_code": contract_code},
            headers=headers
        )
    
    if resp.status_code != 200:
        return {
            "error": "No se pudo obtener información del contrato",
            "detalle": resp.text
        }
    
    # try:
    #     service_data = resp.json()
        
    #     # Obtener form_id desde la respuesta
    #     form_id = service_data.get("id")
                
    # except:
    #     return {"error": "El servicio no devolvió JSON válido."}
    
    
    async with httpx.AsyncClient() as client:

        # Servicio 1
        resp = await client.get(
            external_url,
            params={"contract_code": contract_code},
            headers=headers
        )

        if resp.status_code != 200:
            return {"error": "Error en servicio FORM", "detalle": resp.text}

        # Procesar respuesta
        content_type = resp.headers.get("content-type", "")
        service_data = None
        form_id = None

        if "application/json" in content_type:
            service_data = resp.json()
            form_id = service_data.get("id")
        else:
            service_data = {"html": resp.text}

        # Servicios 2: Emisiones ✅ DENTRO DEL MISMO BLOQUE
        emisiones_data = {}

        if form_id:
            resp_emisiones = await client.get(
                url_emisiones,
                params={"form_id": form_id},
                headers=headers
            )

            if resp_emisiones.status_code == 200:
                try:
                    emisiones_data = resp_emisiones.json()
                except:
                    emisiones_data = {}

    
    
    


    
    
    # print("SERVICE DATA:", service_data)
    
    # -------------------------------
    #  RENDERIZAR TU PLANTILLA HTML
    # -------------------------------
    from datetime import datetime
    
    meses = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    dias = {
        "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
        "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado",
        "Sunday": "domingo"
    }

    now = datetime.now()
    dia = dias[now.strftime("%A")]
    mes = meses[now.month]

    fecha_es = f"{dia} {now.day} de {mes} del {now.year}"


    fecha = datetime.now()
    # Renderizado con Jinja2
    html_renderizado = templates.get_template("contrato_template.html").render(
        data=service_data,
        emisiones=emisiones_data,
        fecha_hora=fecha_es
    )

    # Generar PDF con Playwright
    buffer = await run_in_threadpool(generar_pdf_sync, html_renderizado)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
    )