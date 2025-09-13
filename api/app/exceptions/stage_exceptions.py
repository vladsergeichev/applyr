from .base_exceptions import NotFoundException


class StageNotFoundException(NotFoundException):
    detail = "Этап не найден"
