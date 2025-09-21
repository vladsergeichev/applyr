class VacancyDetailsRenderer {
    constructor() {
        this.container = document.getElementById('vacancies-container');
        this.dropdownInstance = null;
        this.currentVacancyId = null;
        this.setupNotesHandlers();
        this.setupStageSelect();
    }

    // Инициализация выпадающего списка с этапами
    setupStageSelect() {
        const stageSelect = document.getElementById('vacancy-data-stage');
        if (!stageSelect) return;

        // Очищаем текущие опции
        stageSelect.innerHTML = '';

        // Добавляем опции из констант
        Object.entries(VACANCY_STAGES).forEach(([value, label]) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = label;
            stageSelect.appendChild(option);
        });

        // Добавляем обработчик изменения
        stageSelect.addEventListener('change', () => this.updateNotes());
    }

    get vacancyClient() {
        return window.app.vacancyClient;
    }

    get favoriteClient() {
        return window.app.favoriteClient;
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

    // Настройка обработчиков для заметок
    setupNotesHandlers() {
        const saveButton = document.getElementById('update-notes-btn');
        if (saveButton) {
            saveButton.addEventListener('click', () => this.updateNotes());
        }
    }

    // Сохранение заметок
    async updateNotes() {
        if (!this.currentVacancyId) return;

        const favoriteData = {
            notes: document.getElementById('vacancy-data-notes').value.trim(),
            stage: document.getElementById('vacancy-data-stage').value
        };

        try {
            await this.favoriteClient.updateNotes(this.currentVacancyId, favoriteData);
            window.app.messageManager.showSuccess('Изменения сохранены');
        } catch (error) {
            window.app.messageManager.showError('Не удалось сохранить изменения');
        }
    }

    // Отображение детальной информации о вакансии
    async render(vacancyId) {
        try {
            const vacancy = await this.vacancyClient.getVacancy(vacancyId);
            this.currentVacancyId = vacancyId;
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
        document.getElementById('vacancy-data-notes').value = vacancy.notes || '';
        document.getElementById('vacancy-data-stage').value = vacancy.stage || 'nothing';

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
