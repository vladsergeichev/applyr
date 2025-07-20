// Клиент для работы с аутентификацией
class AuthClient extends BaseClient {
    constructor() {
        super('/auth');
    }

    // Регистрация нового пользователя
    async register(userData) {
        return this.post('/register', userData);
    }

    // Вход пользователя
    async login(userData) {
        return this.post('/login', userData);
    }

    // Обновление access токена
    async refreshToken() {
        return this.post('/refresh');
    }

    // Выход пользователя
    async logout() {
        return this.post('/logout');
    }

    // Обновление Telegram username
    async updateTelegramUsername(telegramData) {
        return this.put('/update_telegram', telegramData);
    }
}