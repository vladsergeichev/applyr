// Клиент для работы с пользователями
class UserClient extends BaseClient {
    constructor() {
        super('/users');
    }

    // Создает нового пользователя
    async createUser(userData) {
        return this.post('/create_user', userData);
    }

    // Получает пользователя по ID
    async getUser(userId) {
        return this.get(`/${userId}`);
    }

    // Обновляет данные пользователя
    async updateUser(userId, userData) {
        return this.put(`/${userId}`, userData);
    }
} 