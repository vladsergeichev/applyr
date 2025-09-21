class VacancyDetailsRenderer {
    constructor() {
        this.container = document.getElementById('vacancies-container');
        this.dropdownInstance = null;
    }

    get vacancyClient() {
        return window.app.vacancyClient;
    }

    // Создаем или обновляем дропдаун
    setupDropdown(vacancy) {
        const actionsContainer = document.getElementById('vacancy-actions');
        if (!actionsContainer) return;

        const dropdownItems = [
            {
                text: 'Редактировать',
                onClick: () => window.showVacancyModal({mode: 'edit', vacancy})
            },
            {
                text: 'Удалить',
                className: 'clr-red',
                onClick: () => {
                    showDeleteVacancyConfirm(vacancy, () => {
                        window.app.router.navigate('/');
                    });
                }
            }
        ];

        // Если дропдаун уже существует, обновляем только обработчики
        if (this.dropdownInstance) {
            this.dropdownInstance.updateItems(dropdownItems);
            return;
        }

        // Создаем новый дропдаун
        this.dropdownInstance = new Dropdown({
            items: dropdownItems
        });

        actionsContainer.appendChild(this.dropdownInstance.getContainer());
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
        document.getElementById('vacancy-data-contact-link').href = vacancy.contact_link || vacancy.link;

        // Обновляем дропдаун
        this.setupDropdown(vacancy);
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
