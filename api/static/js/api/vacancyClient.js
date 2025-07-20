// Клиент для работы с вакансиями
class VacancyClient extends BaseClient {
    constructor() {
        super('/vacancy');
    }

    // Получение вакансий текущего пользователя
    async getVacancies() {
        return this.get('/get_vacancies');
    }

    // Создание вакансии
    async createVacancy(vacancyData) {
        return this.post('/create_vacancy', vacancyData);
    }

    // Получение конкретной вакансии
    async getVacancy(vacancyId) {
        return this.get(`/get_vacancy/${vacancyId}`);
    }

    // Обновление вакансии
    async updateVacancy(vacancyId, vacancyData) {
        return this.put(`/update_vacancy/${vacancyId}`, vacancyData);
    }

    // Удаление вакансии
    async deleteVacancy(vacancyId) {
        return this.delete(`/delete_vacancy/${vacancyId}`);
    }
} 