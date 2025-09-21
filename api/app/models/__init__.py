# Импортируем Base для Alembic
from app.database import Base

from .auth import RefreshModel, UserModel
from .favorite import FavoriteModel
from .stage import StageModel
from .vacancy import VacancyModel

__all__ = [
    "Base",
    "UserModel",
    "RefreshModel",
    "VacancyModel",
    "StageModel",
    "FavoriteModel",
]
