// Клиент для работы с откликами
class ApplyClient extends BaseClient {
    constructor() {
        super('/applies');
    }

    // Получает все отклики пользователя по username
    async getApplies(username) {
        return this.get(`/get_applies/${username}`);
    }

    // Создает новый отклик
    async createApply(applyData) {
        return this.post('/create_apply', applyData);
    }

    // Обновляет отклик
    async updateApply(applyId, applyData) {
        return this.put(`/update_apply/${applyId}`, applyData);
    }

    // Удаляет отклик
    async deleteApply(applyId) {
        return this.delete(`/delete_apply/${applyId}`);
    }
} 