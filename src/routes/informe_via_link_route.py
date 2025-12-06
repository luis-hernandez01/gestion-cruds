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

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            external_url,
            params={"contract_code": contract_code},
            headers={"Authorization": f"Bearer {token}"}
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="No se encontró el contrato")

    # JSON del servicio
    try:
        service_data = resp.json()
    except:
        raise HTTPException(status_code=400, detail="El servicio no devolvió JSON válido")

    # Renderizado con Jinja2
    html_renderizado = templates.get_template("contrato_template.html").render(
        data=service_data
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