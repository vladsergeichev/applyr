from .base_exceptions import NotFoundException


class VacancyNotFoundException(NotFoundException):
    detail = "Вакансия не найдена"
