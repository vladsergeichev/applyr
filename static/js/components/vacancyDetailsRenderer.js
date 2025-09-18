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
        document.getElementById('vacancy-data-title').innerHTML = vacancy.name;
        document.getElementById('vacancy-data-name').innerHTML = vacancy.name;
        document.getElementById('vacancy-data-company').innerHTML = vacancy.company_name || '–';
        document.getElementById('vacancy-data-salary').innerHTML = vacancy.salary || '';
        document.getElementById('vacancy-data-experience').innerHTML = vacancy.experience || '–';
        document.getElementById('vacancy-data-location').innerHTML = vacancy.location || '–';
        document.getElementById('vacancy-data-employment').innerHTML = vacancy.employment || '–';
        document.getElementById('vacancy-data-description').innerHTML = (vacancy.description || '–').replace(/\n/g, '<br>');
        document.getElementById('vacancy-data-requirements').innerHTML = (vacancy.requirements || '–').replace(/\n/g, '<br>');
        document.getElementById('vacancy-data-conditions').innerHTML = (vacancy.conditions || '–').replace(/\n/g, '<br>');
        document.getElementById('vacancy-data-link').href = vacancy.link;

        // Добавляем дропдаун с действиями
        const actionsContainer = document.getElementById('vacancy-actions');
        const dropdown = new Dropdown({
            items: [
                {
                    text: 'Редактировать',
                    onClick: () => window.showVacancyModal({mode: 'edit', vacancy})
                },
                {
                    text: 'Удалить',
                    className: 'clr-red',
                    onClick: async () => {
                        if (confirm('Вы уверены, что хотите удалить эту вакансию?')) {
                            try {
                                await this.vacancyClient.deleteVacancy(vacancy.id);
                                window.app.messageManager.showSuccess('Вакансия удалена!');
                                window.app.router.navigate('/');
                            } catch (err) {
                                window.app.messageManager.showError('Ошибка при удалении вакансии');
                            }
                        }
                    }
                }
            ]
        });

        actionsContainer.appendChild(dropdown.getContainer());
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
