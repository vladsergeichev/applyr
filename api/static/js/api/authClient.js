// Клиент для работы с аутентификацией
class AuthClient extends BaseClient {
    constructor() {
        super('/auth');
    }

    // Валидация данных пользователя
    _validateUserData(userData) {
        if (!userData || typeof userData !== 'object') {
            throw new Error(ERROR_MESSAGES.INVALID_USER_DATA);
        }
    }

    // Валидация данных Telegram
    _validateTelegramData(telegramData) {
        if (!telegramData || typeof telegramData !== 'object') {
            throw new Error(ERROR_MESSAGES.INVALID_USER_DATA);
        }
    }

    // Регистрация нового пользователя
    async register(userData) {
        this._validateUserData(userData);
        return this.post('/register', userData);
    }

    // Вход пользователя
    async login(userData) {
        this._validateUserData(userData);
        return this.post('/login', userData);
    }

    // Обновление access токена
    async refreshToken() {
        return await this.request('/refresh', {
            method: 'POST',
            credentials: 'include',
        }, true);
    }

    // Выход пользователя
    async logout() {
        return await this.request('/logout', {
            method: 'POST',
            credentials: 'include',
        }, true);
    }

    // Обновление Telegram username
    async updateTelegramUsername(telegramData) {
        this._validateTelegramData(telegramData);
        return this.put('/update_telegram', telegramData);
    }
}