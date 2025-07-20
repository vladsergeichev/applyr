// Клиент для работы с этапами вакансий
class StageClient extends BaseClient {
    constructor() {
        super('/stage');
    }

    // Валидация ID этапа
    _validateStageId(stageId) {
        if (!stageId || typeof stageId !== 'string' && typeof stageId !== 'number') {
            throw new Error(ERROR_MESSAGES.INVALID_ID);
        }
    }

    // Валидация ID вакансии
    _validateVacancyId(vacancyId) {
        if (!vacancyId || typeof vacancyId !== 'string' && typeof vacancyId !== 'number') {
            throw new Error(ERROR_MESSAGES.INVALID_ID);
        }
    }

    // Валидация данных этапа
    _validateStageData(stageData) {
        if (!stageData || typeof stageData !== 'object') {
            throw new Error(ERROR_MESSAGES.INVALID_STAGE_DATA);
        }
    }

    // Получает все этапы вакансии
    async getStages(vacancyId) {
        this._validateVacancyId(vacancyId);
        return this.get(`/get_stages/${vacancyId}`);
    }

    // Создает новый этап
    async createStage(stageData) {
        this._validateStageData(stageData);
        return this.post('/create_stage', stageData);
    }

    // Получает этап по ID
    async getStage(stageId) {
        this._validateStageId(stageId);
        return this.get(`/get_stage/${stageId}`);
    }

    // Обновляет этап
    async updateStage(stageId, stageData) {
        this._validateStageId(stageId);
        this._validateStageData(stageData);
        return this.put(`/update_stage/${stageId}`, stageData);
    }

    // Удаляет этап
    async deleteStage(stageId) {
        this._validateStageId(stageId);
        return this.delete(`/delete_stage/${stageId}`);
    }
} 