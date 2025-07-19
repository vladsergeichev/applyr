class AuthError(Exception):
    """Базовое исключение для аутентификации"""

    pass


class UserAlreadyExistsError(AuthError):
    """Пользователь уже существует"""

    pass


class InvalidCredentialsError(AuthError):
    """Неверные учетные данные"""

    pass


class TokenExpiredError(AuthError):
    """Токен истек"""

    pass


class TokenInvalidError(AuthError):
    """Недействительный токен"""

    pass


class UserNotFoundError(AuthError):
    """Пользователь не найден"""

    pass
