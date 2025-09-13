import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Обработчик для ошибок валидации Pydantic"""
    logger.warning(f"Validation Error: {exc.errors()}")

    # Преобразуем ошибки в сериализуемый формат
    serializable_errors = []
    for error in exc.errors():
        serializable_error = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
            "input": str(error["input"]) if error.get("input") is not None else None,
        }
        if "ctx" in error and "error" in error["ctx"]:
            serializable_error["ctx"] = {"error": str(error["ctx"]["error"])}
        serializable_errors.append(serializable_error)

    return JSONResponse(
        status_code=422,
        content={"detail": "Ошибка валидации данных", "errors": serializable_errors},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики исключений"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
