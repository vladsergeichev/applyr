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
            <h3 style="display:inline;vertical-align:middle;">Мои вакансии</h3>
            <span class="vacancies-count-simple">${vacancies.length}</span>
        `;
        return header;
    }

    // Создает сетку вакансий (без внешнего контейнера с рамкой)
    createVacanciesGrid(vacancies) {
        const grid = document.createElement('div');
        grid.className = 'vacancies-list-items vacancies-list-items--fullwidth';
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

        // Цвета для статусов
        const statusColors = {
            active: '#22c55e',
            closed: '#ef4444',
            draft: '#a3a3a3',
            interview: '#3b82f6',
            offer: '#f59e42',
        };
        const status = vacancy.status || 'active';
        const statusColor = statusColors[status] || '#a3a3a3';
        const statusLabel = `<span class="vacancy-status-label" style="background:${statusColor}">${this.escapeHtml(status)}</span>`;

        // Название и компания
        const title = `<span class="vacancy-title">${this.escapeHtml(vacancy.name)}</span>`;
        const company = `<span class="vacancy-company">${this.escapeHtml(vacancy.company_name || '<название компании>')}</span>`;

        // Иконки
        const linkIcon = vacancy.link ?
            `<a href="${this.escapeHtml(vacancy.link)}" target="_blank" class="vacancy-action-btn" title="Открыть вакансию">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            </a>` : '';
        const editIcon = `<button class="vacancy-action-btn" title="Редактировать" disabled style="opacity:0.5;cursor:default">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>
        </button>`;
        const deleteIcon = `<button class="vacancy-action-btn delete-btn" onclick="showDeleteVacancyModal(${vacancy.id})" title="Удалить вакансию">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
        </button>`;

        item.innerHTML = `
            <div class="vacancy-card-layout">
                <div class="vacancy-card-left">${statusLabel}</div>
                <div class="vacancy-card-center">${title}${company}</div>
                <div class="vacancy-card-right">${linkIcon}${editIcon}${deleteIcon}</div>
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