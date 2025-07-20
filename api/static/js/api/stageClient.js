// Клиент для работы с этапами вакансий
class StageClient extends BaseClient {
    constructor() {
        super('/stage');
    }

    // Получает все этапы вакансии
    async getStages(vacancyId) {
        return this.get(`/get_stages/${vacancyId}`);
    }

    // Создает новый этап
    async createStage(stageData) {
        return this.post('/create_stage', stageData);
    }

    // Получает этап по ID
    async getStage(stageId) {
        return this.get(`/get_stage/${stageId}`);
    }

    // Обновляет этап
    async updateStage(stageId, stageData) {
        return this.put(`/update_stage/${stageId}`, stageData);
    }

    // Удаляет этап
    async deleteStage(stageId) {
        return this.delete(`/delete_stage/${stageId}`);
    }
} 