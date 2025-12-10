from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from pathlib import Path
from src.utils.jwt_validator_util import verify_jwt_token, others_verify_jwt_token
from fastapi import APIRouter, Depends
import httpx


router_DIR = Path(__file__).parent
STORAGE_DIR = router_DIR / "html_storage"
STORAGE_DIR.mkdir(exist_ok=True)
router = APIRouter()

templates = Jinja2Templates(directory=str(router_DIR / "templates"))

@router.get("/contract-to-html/{contract_code}")
async def contract_to_html(
    contract_code: str,
    request: Request,
    tokenpayload: dict = Depends(others_verify_jwt_token)
):

    # Obtener token original
    token = tokenpayload.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Llamada al servicio externo
    external_url = "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/form/by-contract-code"
    url_emisiones = "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/api/v1/emissions"
    
    url_quarterly = "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/api/v1/quarterly-reports/"
    
    url_monthly = "https://as-aikawayra-wayra-dev-b2-eastus.azurewebsites.net/api/v1/monthly-reports/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/html"
    }

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
        id = None

        if "application/json" in content_type:
            service_data = resp.json()
            form_id = service_data.get("id")
            # id = service_data.get("id")
        else:
            service_data = {"html": resp.text}

        # Servicios 2: Emisiones DENTRO DEL MISMO BLOQUE
        emisiones_data = {}
        quarterly_data = {}
        monthly_data = {}
        
        # if id:
        #     resp_quarterly = await client.get(
        #         url_quarterly,
        #         params={"id": id},
        #         headers=headers
        #     )
            
        #     if resp_quarterly.status_code == 200:
        #         try:
        #             quarterly_data = resp_quarterly.json()
        #         except:
        #             quarterly_data = {}

        if form_id:
            resp_quarterly = await client.get(
                url_quarterly,
                params={"form_id": form_id},
                headers=headers
            )
            
            if resp_quarterly.status_code == 200:
                try:
                    quarterly_data = resp_quarterly.json()
                except:
                    quarterly_data = {}
                    
                    
            resp_emisiones = await client.get(
                url_emisiones,
                params={"form_id": form_id},
                headers=headers
            )
            
            resp_monthly = await client.get(
                url_monthly,
                params={"form_id": form_id},
                headers=headers
            )
            
            if resp_monthly.status_code == 200:
                try:
                    monthly_data = resp_monthly.json()
                except:
                    monthly_data = {}

            if resp_emisiones.status_code == 200:
                try:
                    emisiones_data = resp_emisiones.json()
                except:
                    emisiones_data = {}
                    
                    
                    
        
                    
                    
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
        monthly=monthly_data,
        quarterly=quarterly_data,
        fecha_hora=fecha_es
    )

    # Guardar el HTML igual que upload-html
    item_id = uuid4().hex
    file_path = STORAGE_DIR / f"{item_id}.html"
    file_path.write_text(html_renderizado, encoding="utf-8")

    return {
        "id": item_id,
        "raw": request.url_for("raw_contract_html", item_id=item_id),
        "preview": request.url_for("preview_contract_html", item_id=item_id)
    }




@router.get("/raw-contract/{item_id}", response_class=HTMLResponse, name="raw_contract_html")
def raw_contract_html(item_id: str):
    file_path = STORAGE_DIR / f"{item_id}.html"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="No encontrado")

    return HTMLResponse(content=file_path.read_text(encoding="utf-8"))



@router.get("/preview-contract/{item_id}", name="preview_contract_html")
def preview_contract_html(item_id: str, request: Request):
    url_html = request.url_for("raw_contract_html", item_id=item_id)

    return templates.TemplateResponse(
        "viewer.html",
        {
            "request": request,
            "url_html": url_html
        }
    )