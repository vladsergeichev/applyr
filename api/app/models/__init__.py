# Импортируем Base для Alembic
from app.database import Base

from .auth import RefreshModel, UserModel
from .stage import StageModel
from .vacancy import VacancyModel
from .favorite import FavoriteModel

__all__ = [
    "Base",
    "UserModel",
    "RefreshModel",
    "VacancyModel",
    "StageModel",
    "FavoriteModel",
]
