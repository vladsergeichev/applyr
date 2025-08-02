// Клиент для работы с вакансиями
class VacancyClient extends BaseClient {
    constructor() {
        super('/vacancy');
    }

    // Валидация ID вакансии
    _validateVacancyId(vacancyId) {
        if (!vacancyId || typeof vacancyId !== 'string' && typeof vacancyId !== 'number') {
            throw new Error(ERROR_MESSAGES.INVALID_ID);
        }
    }

    // Валидация данных вакансии
    _validateVacancyData(vacancyData) {
        if (!vacancyData || typeof vacancyData !== 'object') {
            throw new Error(ERROR_MESSAGES.INVALID_VACANCY_DATA);
        }
    }

    // Получение вакансий текущего пользователя
    async getVacancies() {
        return this.get('/get_vacancies');
    }

    // Создание вакансии
    async createVacancy(vacancyData) {
        this._validateVacancyData(vacancyData);
        return this.post('/create_vacancy', vacancyData);
    }

    // Получение конкретной вакансии
    async getVacancy(vacancyId) {
        this._validateVacancyId(vacancyId);
        return this.get(`/get_vacancy/${vacancyId}`);
    }

    // Обновление вакансии
    async updateVacancy(vacancyId, vacancyData) {
        this._validateVacancyId(vacancyId);
        this._validateVacancyData(vacancyData);
        return this.put(`/update_vacancy/${vacancyId}`, vacancyData);
    }

    // Удаление вакансии
    async deleteVacancy(vacancyId) {
        this._validateVacancyId(vacancyId);
        return this.delete(`/delete_vacancy/${vacancyId}`);
    }
} 