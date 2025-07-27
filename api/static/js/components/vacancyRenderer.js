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
        // Внешний контейнер
        const outer = document.createElement('div');
        outer.className = 'vacancy-card-outer';

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
            `<a href="${this.escapeHtml(vacancy.link)}" target="_blank" class="vacancy-action-btn" title="Открыть вакансию" onclick="event.stopPropagation()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            </a>` : '';
        const editIcon = `<button class="vacancy-action-btn" title="Редактировать" disabled style="opacity:0.5;cursor:default" onclick="event.stopPropagation()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>
        </button>`;
        const deleteIcon = `<button class="vacancy-action-btn delete-btn" onclick="event.stopPropagation();showDeleteVacancyModal(${vacancy.id})" title="Удалить вакансию">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
        </button>`;

        item.innerHTML = `
            <div class="vacancy-card-layout">
                <div class="vacancy-card-left">${statusLabel}</div>
                <div class="vacancy-card-center">${title}${company}</div>
                <div class="vacancy-card-right">${linkIcon}${editIcon}${deleteIcon}</div>
            </div>
        `;

        // Функция для рендера этапов
        async function renderStagesBlock() {
            document.querySelectorAll('.vacancy-stages-block').forEach(el => el.remove());
            let stages = [];
            try {
                stages = await app.stageClient.getStages(vacancy.id);
            } catch (err) {
                app.messageManager.showError('Ошибка загрузки этапов');
            }
            const stagesBlock = document.createElement('div');
            stagesBlock.className = 'vacancy-stages-block';
            (stages || []).forEach(stage => {
                const stageDiv = document.createElement('div');
                stageDiv.className = 'stage-item';
                stageDiv.textContent = stage.description;
                // Кнопка удаления
                const delBtn = document.createElement('button');
                delBtn.className = 'stage-delete-btn';
                delBtn.title = 'Удалить этап';
                delBtn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>`;
                delBtn.onclick = function(e) {
                    e.stopPropagation();
                    showDeleteStageModal(stage.id, renderStagesBlock);
                };
                stageDiv.appendChild(delBtn);
                stagesBlock.appendChild(stageDiv);
            });
            // + Добавить
            const addRow = document.createElement('div');
            addRow.className = 'stage-add-row';
            const addBtn = document.createElement('span');
            addBtn.className = 'stage-add-btn';
            addBtn.textContent = '+ Добавить';
            addRow.appendChild(addBtn);
            stagesBlock.appendChild(addRow);
            // Логика добавления этапа
            addBtn.addEventListener('click', function() {
                if (stagesBlock.querySelector('.stage-add-input')) return;
                addBtn.style.display = 'none';
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'stage-add-input';
                input.placeholder = 'Название этапа';
                input.autofocus = true;
                addBtn.parentNode.appendChild(input);
                input.focus();
                let finished = false;
                async function finishAdd() {
                    if (finished) return;
                    finished = true;
                    input.removeEventListener('blur', finishAdd);
                    input.removeEventListener('keydown', onKeyDown);
                    const value = input.value.trim();
                    if (value) {
                        try {
                            await app.stageClient.createStage({ vacancy_id: vacancy.id, stage_type: "active", description: value });
                            await renderStagesBlock(); // перерисовать этапы после добавления
                        } catch (err) {
                            app.messageManager.showError('Ошибка добавления этапа');
                        }
                    }
                    input.remove();
                    addBtn.style.display = '';
                }
                function onKeyDown(e) {
                    if (e.key === 'Enter') finishAdd();
                    if (e.key === 'Escape') { input.remove(); addBtn.style.display = ''; }
                }
                input.addEventListener('keydown', onKeyDown);
                input.addEventListener('blur', finishAdd);
            });
            // Удаляем старый блок и добавляем новый
            document.querySelectorAll('.vacancy-stages-block').forEach(el => el.remove());
            outer.appendChild(stagesBlock);
        }

        item.addEventListener('click', function(e) {
            if (e.target.closest('.vacancy-action-btn')) return;
            const next = outer.querySelector('.vacancy-stages-block');
            if (next) { next.remove(); return; }
            renderStagesBlock();
        });

        outer.appendChild(item);
        return outer;
    }

    // Экранирует HTML для безопасности
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Модалка подтверждения удаления этапа
function showDeleteStageModal(stageId, onSuccess) {
    if (document.getElementById('delete-stage-modal')) return;
    const modal = document.createElement('div');
    modal.className = 'modal show';
    modal.id = 'delete-stage-modal';
    modal.innerHTML = `
        <div class=\"modal-content\" style=\"max-width:340px;text-align:center;\">
            <div class=\"modal-header\"><h2>Удалить этап?</h2></div>
            <div class=\"modal-body\" style=\"margin:1.2em 0 2em 0;\">Вы уверены, что хотите удалить этап?</div>
            <div class=\"modal-footer\" style=\"display:flex;gap:1em;justify-content:center;\">
                <button class=\"btn btn-danger\" id=\"confirm-delete-stage\">Удалить</button>
                <button class=\"btn btn-secondary\" id=\"cancel-delete-stage\">Отмена</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    document.getElementById('confirm-delete-stage').onclick = async function() {
        try {
            await app.stageClient.deleteStage(stageId);
            if (onSuccess) await onSuccess();
        } catch (err) {
            app.messageManager.showError('Ошибка удаления этапа');
        }
        closeDeleteStageModal();
    };
    document.getElementById('cancel-delete-stage').onclick = closeDeleteStageModal;
    modal.onclick = function(e) { if (e.target === modal) closeDeleteStageModal(); };
}
function closeDeleteStageModal() {
    const modal = document.getElementById('delete-stage-modal');
    if (modal) modal.remove();
} 