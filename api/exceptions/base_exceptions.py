from fastapi import HTTPException, status


class AppException(HTTPException):
    """Базовый класс для всех исключений приложения"""

    def __init__(self, status_code: int = None, detail: str = None):
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail)


class ValidationException(AppException):
    """Исключение для ошибок валидации"""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Ошибка валидации данных"


class NotFoundException(AppException):
    """Исключение для ресурсов, которые не найдены"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ресурс не найден"


class ConflictException(AppException):
    """Исключение для конфликтов (дублирование, несовместимость)"""

    status_code = status.HTTP_409_CONFLICT
    detail = "Конфликт данных"


class UnauthorizedException(AppException):
    """Исключение для ошибок авторизации"""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не авторизован"


class ForbiddenException(AppException):
    """Исключение для ошибок доступа"""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ запрещен"
