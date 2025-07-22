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
        grid.className = 'vacancies-list-items';

        vacancies.forEach(vacancy => {
            const vacancyItem = this.createVacancyItem(vacancy);
            grid.appendChild(vacancyItem);
        });

        return grid;
    }

    // Создает элемент вакансии в виде списка
    createVacancyItem(vacancy) {
        const item = document.createElement('div');
        item.className = 'vacancy-item';
        item.dataset.vacancyId = vacancy.id;

        const linkIcon = vacancy.link ? 
            '<svg class="vacancy-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>' : 
            '<svg class="vacancy-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><path d="M21 12c-1 0-2.4-.4-3.5-1.5S16 9 16 8s.4-2.5 1.5-3.5S20 3 21 3s2.4.4 3.5 1.5S26 7 26 8s-.4 2.5-1.5 3.5S22 12 21 12z"/></svg>';

        const title = vacancy.link ? 
            `<a href="${this.escapeHtml(vacancy.link)}" target="_blank" class="vacancy-title">${this.escapeHtml(vacancy.name)}</a>` :
            `<span class="vacancy-title">${this.escapeHtml(vacancy.name)}</span>`;

        item.innerHTML = `
            <div class="vacancy-content">
                ${linkIcon}
                ${title}
            </div>
            <div class="vacancy-actions">
                <button class="delete-btn" onclick="deleteVacancy(${vacancy.id})" title="Удалить вакансию">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
                    </svg>
                </button>
            </div>
        `;

        return item;
    }

    // Экранирует HTML для безопасности
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
} 