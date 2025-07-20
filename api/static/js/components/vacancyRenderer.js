// Рендерер для отображения вакансий
class VacancyRenderer {
    constructor() {
        this.vacanciesList = document.getElementById('vacancies-list');
        this.noVacancies = document.getElementById('no-vacancies');
    }

    // Очищает контейнер вакансий
    clear() {
        this.vacanciesList.innerHTML = '';
        this.vacanciesList.classList.add('hidden');
        this.noVacancies.classList.add('hidden');
    }

    // Показывает сообщение об отсутствии вакансий
    showNoVacancies() {
        this.clear();
        this.noVacancies.classList.remove('hidden');
    }

    // Показывает ошибку загрузки
    showError(message) {
        this.clear();
        this.vacanciesList.innerHTML = `
            <div class="error-vacancies">
                <div class="error-icon">⚠️</div>
                <p>${message}</p>
            </div>
        `;
        this.vacanciesList.classList.remove('hidden');
    }

    // Показывает индикатор загрузки
    showLoading() {
        this.clear();
        this.vacanciesList.innerHTML = `
            <div class="loading-vacancies">
                <div class="spinner"></div>
                <p>Загрузка вакансий...</p>
            </div>
        `;
        this.vacanciesList.classList.remove('hidden');
    }

    // Рендерит список вакансий
    renderVacancies(vacancies, username) {
        this.clear();

        if (!vacancies || vacancies.length === 0) {
            this.showNoVacancies();
            return;
        }

        const header = this.createVacanciesHeader(vacancies, username);
        const grid = this.createVacanciesGrid(vacancies);

        this.vacanciesList.appendChild(header);
        this.vacanciesList.appendChild(grid);
        this.vacanciesList.classList.remove('hidden');
    }

    // Создает заголовок списка вакансий
    createVacanciesHeader(vacancies, username) {
        const header = document.createElement('div');
        header.className = 'vacancies-header';
        header.innerHTML = `
            <h3>Мои вакансии</h3>
            <div class="vacancies-count">${vacancies.length} вакансий</div>
        `;
        return header;
    }

    // Создает сетку вакансий
    createVacanciesGrid(vacancies) {
        const grid = document.createElement('div');
        grid.className = 'vacancies-grid';

        vacancies.forEach(vacancy => {
            const vacancyCard = this.createVacancyCard(vacancy);
            grid.appendChild(vacancyCard);
        });

        return grid;
    }

    // Создает карточку вакансии
    createVacancyCard(vacancy) {
        const card = document.createElement('div');
        card.className = 'vacancy-item';
        card.dataset.vacancyId = vacancy.id;

        const date = new Date(vacancy.created_at).toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        card.innerHTML = `
            <div class="vacancy-header">
                <div class="vacancy-title">${this.escapeHtml(vacancy.name)}</div>
                <div class="vacancy-actions">
                    <button class="delete-btn" onclick="deleteVacancy(${vacancy.id})" title="Удалить вакансию">
                        🗑️
                    </button>
                </div>
            </div>
            <div class="vacancy-meta">
                <div class="vacancy-date">Создана: ${date}</div>
            </div>
            ${vacancy.link ? `
                <div class="vacancy-link-container">
                    <a href="${this.escapeHtml(vacancy.link)}" target="_blank" class="vacancy-link">
                        🔗 Открыть вакансию
                    </a>
                </div>
            ` : ''}
            ${vacancy.description ? `
                <div class="vacancy-description">
                    ${this.escapeHtml(vacancy.description)}
                </div>
            ` : ''}
            ${vacancy.company_name ? `
                <div class="vacancy-company">
                    <strong>Компания:</strong> ${this.escapeHtml(vacancy.company_name)}
                </div>
            ` : ''}
        `;

        return card;
    }

    // Экранирует HTML для безопасности
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
} 