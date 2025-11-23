from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from playwright.sync_api import sync_playwright
from starlette.concurrency import run_in_threadpool

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)

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


@router.post("/html-to-pdf")
async def html_to_pdf(file: UploadFile = File(...)):
    html_content = (await file.read()).decode("utf-8")

    # Ejecutamos Playwright Sync en un hilo aparte
    buffer = await run_in_threadpool(generar_pdf_sync, html_content)

    return StreamingResponse(
        buffer,
        media_type="routerlication/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
    )
