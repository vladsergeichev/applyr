// Клиент для работы с вакансиями
class VacancyClient extends BaseClient {
    constructor() {
        super('/vacancy');
    }

    // Получает все вакансии пользователя по username
    async getVacancies(username) {
        return this.get(`/get_vacancies/${username}`);
    }

    // Создает новую вакансию
    async createVacancy(vacancyData) {
        return this.post('/create_vacancy', vacancyData);
    }

    // Получает вакансию по ID
    async getVacancy(vacancyId) {
        return this.get(`/get_vacancy/${vacancyId}`);
    }

    // Обновляет вакансию
    async updateVacancy(vacancyId, vacancyData) {
        return this.put(`/update_vacancy/${vacancyId}`, vacancyData);
    }

    // Удаляет вакансию
    async deleteVacancy(vacancyId) {
        return this.delete(`/delete_vacancy/${vacancyId}`);
    }
} 