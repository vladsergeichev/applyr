from config import templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Возвращает главную HTML-страницу"""
    return templates.TemplateResponse(
        "main.html",
        {"request": request},
    )
