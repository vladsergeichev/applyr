from .auth_exceptions import (
    InvalidCredentialsException,
    TelegramUsernameAlreadyExistsException,
    TokenExpiredException,
    TokenInvalidException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from .base_exceptions import (
    AppException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from .stage_exceptions import (
    StageNotFoundException,
)
from .vacancy_exceptions import (
    VacancyNotFoundException,
)

__all__ = [
    # Base exceptions
    "AppException",
    "ValidationException",
    "NotFoundException",
    "ConflictException",
    "UnauthorizedException",
    "ForbiddenException",
    # Auth exceptions
    "UserAlreadyExistsException",
    "InvalidCredentialsException",
    "TokenExpiredException",
    "TokenInvalidException",
    "UserNotFoundException",
    "TelegramUsernameAlreadyExistsException",
    # Vacancy exceptions
    "VacancyNotFoundException",
    # Stage exceptions
    "StageNotFoundException",
]
