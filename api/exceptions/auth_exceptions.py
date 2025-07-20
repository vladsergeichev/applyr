from .base_exceptions import (
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)


class UserAlreadyExistsException(ConflictException):
    detail = "Пользователь с таким username уже существует"


class InvalidCredentialsException(UnauthorizedException):
    detail = "Неверный username или пароль"


class TokenExpiredException(UnauthorizedException):
    detail = "Токен истек"


class TokenInvalidException(UnauthorizedException):
    detail = "Недействительный токен"


class UserNotFoundException(NotFoundException):
    detail = "Пользователь не найден"


class TelegramUsernameAlreadyExistsException(ConflictException):
    detail = "Telegram username уже используется"
