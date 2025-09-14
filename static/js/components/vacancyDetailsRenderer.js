class VacancyDetailsRenderer {
    constructor() {
        this.container = document.getElementById('vacancies-container');
    }

    get vacancyClient() {
        return window.app.vacancyClient;
    }

    // Отображение детальной информации о вакансии
    async render(vacancyId) {
        try {
            const vacancy = await this.vacancyClient.getVacancy(vacancyId);
            this.renderVacancyDetails(vacancy);
            document.getElementById('vacancies-container').classList.add('hidden');
        } catch (error) {
            this.showError('Не удалось загрузить информацию о вакансии');
        }
    }

    // Заполнение страницы информацией
    renderVacancyDetails(vacancy) {
        document.getElementById('vacancy-data-name').innerHTML = vacancy.name;
        document.getElementById('vacancy-data-company').innerHTML = vacancy.company_name;
        document.getElementById('vacancy-data-description').innerHTML = vacancy.description.replace(/\n/g, '<br>');
    }

    // Отображение ошибки
    showError(message) {
        this.container.innerHTML = `
            <div class="error-container">
                <div class="error-icon">⚠️</div>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.app.router.navigate('/')">
                    Вернуться к списку
                </button>
            </div>
        `;
    }
}
