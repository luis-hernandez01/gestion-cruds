# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import StreamingResponse
# from concurrent.futures import ThreadPoolExecutor
# from io import BytesIO
# from playwright.sync_api import sync_playwright
# from starlette.concurrency import run_in_threadpool

# router = APIRouter()

# executor = ThreadPoolExecutor(max_workers=2)

# def generar_pdf_sync(html: str):
#     buffer = BytesIO()

#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()

#         page.set_content(html, wait_until="load")

#         pdf_bytes = page.pdf(
#         format="A4",
#         print_background=True,
#         display_header_footer=True,
#         margin={"top": "60px", "bottom": "60px", "left": "20px", "right": "20px"},
#         header_template="""
#             <div style="font-size:10px; width:100%; text-align:center; margin-top:10px;">
#                 <span class="date"></span> — <span class="title"></span>
#             </div>
#         """,
#         footer_template="""
#             <div style="font-size:10px; width:100%; text-align:center; margin-bottom:10px;">
#                 Página <span class="pageNumber"></span> de <span class="totalPages"></span>
#             </div>
#         """
#         )

#         buffer.write(pdf_bytes)
#         buffer.seek(0)

#         browser.close()

#     return buffer


# @router.post("/html-to-pdf")
# async def html_to_pdf(file: UploadFile = File(...)):
#     html_content = (await file.read()).decode("utf-8")

#     # Ejecutamos Playwright Sync en un hilo aparte
#     buffer = await run_in_threadpool(generar_pdf_sync, html_content)

#     return StreamingResponse(
#         buffer,
#         media_type="routerlication/pdf",
#         headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
#     )






















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
    
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/html"
    }
    
    # Llamada al servicio externo
    async with httpx.AsyncClient() as client:
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
    try:
        service_data = resp.json()
    except:
        return {"error": "El servicio no devolvió JSON válido."}
    
    
    # print("SERVICE DATA:", service_data)
    
    # -------------------------------
    #  RENDERIZAR TU PLANTILLA HTML
    # -------------------------------
    html_renderizado = templates.get_template("contrato_template.html").render(
        data=service_data
    )

    # Generar PDF con Playwright
    buffer = await run_in_threadpool(generar_pdf_sync, html_renderizado)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
    )