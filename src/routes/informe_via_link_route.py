from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from pathlib import Path

router_DIR = Path(__file__).parent
STORAGE_DIR = router_DIR / "html_storage"
STORAGE_DIR.mkdir(exist_ok=True)

router = APIRouter()

templates = Jinja2Templates(directory=str(router_DIR / "templates"))


@router.post("/upload-html")
async def upload_html(
    request: Request,
    html_text: str | None = Form(None),
    html_file: UploadFile | None = File(None),
):
    if html_text is None and html_file is None:
        raise HTTPException(status_code=400, detail="Necesitas enviar html_text o html_file")

    if html_file:
        content = (await html_file.read()).decode("utf-8")
    else:
        content = html_text

    item_id = uuid4().hex
    file_path = STORAGE_DIR / f"{item_id}.html"
    file_path.write_text(content, encoding="utf-8")

    preview_url = request.url_for("raw", item_id=item_id)

    return {"id": item_id, "raw": preview_url}


@router.get("/raw/{item_id}", response_class=HTMLResponse, name="raw")
def raw_html(item_id: str):
    """
    Devuelve el HTML puro (lo que irá dentro del iframe)
    """
    file_path = STORAGE_DIR / f"{item_id}.html"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="No encontrado")

    return HTMLResponse(content = file_path.read_text(encoding="utf-8", errors="replace"))


@router.get("/preview/{item_id}", name="preview_page")
def preview(item_id: str, request: Request):
    """
    Muestra OTRA PÁGINA con un diseño para visualizar el HTML
    """
    return templates.TemplateResponse(
        "viewer.html",
        {
            "request": request,
            "url_html": request.url_for("raw_html", item_id=item_id)
        }
    )
