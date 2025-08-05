// Рендерер для отображения вакансий
class VacancyRenderer {
    constructor() {
        this.vacanciesList = document.getElementById('vacancies-list');
    }

    // Очищает контейнер вакансий
    clear() {
        this.vacanciesList.innerHTML = '';
        this.vacanciesList.classList.add('hidden');
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
    renderVacancies(vacancies) {
        this.clear();

        const header = this.createVacanciesHeader(vacancies.length);
        const grid = this.createVacanciesGrid(vacancies);

        this.vacanciesList.appendChild(header);
        this.vacanciesList.appendChild(grid);
        this.vacanciesList.classList.remove('hidden');
    }

    // Создает заголовок списка вакансий
    createVacanciesHeader(vacancies_length) {
        const header = document.createElement('div');
        header.className = 'vacancies-header';
        header.innerHTML = `
            <h3 style="display:inline;vertical-align:middle;">Мои вакансии</h3>
            <span class="vacancies-count-simple">${vacancies_length}</span>
            <button class="btn btn-primary add-vacancy-btn" style="margin-left:auto;">+ Добавить вакансию</button>
        `;
        header.querySelector('.add-vacancy-btn').onclick = () => showVacancyModal({ mode: 'add' });
        return header;
    }

    // Создает сетку вакансий
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

        const lastStage = Array.isArray(vacancy.stages) && vacancy.stages.length > 0 ? vacancy.stages[vacancy.stages.length - 1] : null;
        const status = lastStage && lastStage.stage_type ? lastStage.stage_type : 'new';
        const statusColor = STATUS_COLORS[status];
        const statusLabel = `<span class="vacancy-status-label" style="background:${statusColor}">${this.escapeHtml(status)}</span>`;

        // Название и компания
        const title = `<span class="vacancy-title">${this.escapeHtml(vacancy.name)}</span>`;
        const company = `<span class="vacancy-company">${this.escapeHtml(vacancy.company_name || '<название компании>')}</span>`;

        // Иконки
        const linkIcon = vacancy.link ?
            `<a href="${this.escapeHtml(vacancy.link)}" target="_blank" class="vacancy-action-btn vacancy-link-btn" title="Открыть вакансию">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            </a>` : '';
        // Кнопка редактирования через JS
        const editBtn = document.createElement('button');
        editBtn.className = 'vacancy-action-btn vacancy-edit-btn';
        editBtn.title = 'Редактировать';
        editBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>`;
        editBtn.onclick = (e) => {
            e.stopPropagation();
            console.log('Редактировать', vacancy);
            window.showVacancyModal({mode: 'edit', vacancy});
        };
        // Кнопка удаления
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'vacancy-action-btn delete-btn';
        deleteBtn.title = 'Удалить вакансию';
        deleteBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>`;
        deleteBtn.onclick = (e) => { e.stopPropagation(); showDeleteVacancyModal(vacancy.id); };

        item.innerHTML = `
            <div class="vacancy-card-layout">
                <div class="vacancy-card-left">${statusLabel}</div>
                <div class="vacancy-card-center">${title}${company}</div>
                <div class="vacancy-card-right"></div>
            </div>
        `;
        const right = item.querySelector('.vacancy-card-right');
        // Ссылка
        if (vacancy.link) {
            const linkA = document.createElement('a');
            linkA.href = vacancy.link;
            linkA.target = '_blank';
            linkA.className = 'vacancy-action-btn vacancy-link-btn';
            linkA.title = 'Открыть вакансию';
            linkA.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`;
            right.appendChild(linkA);
        }
        // Кнопка редактирования
        right.appendChild(editBtn);
        // Кнопка удаления
        right.appendChild(deleteBtn);

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
                
                // Дата
                const dateDiv = document.createElement('div');
                dateDiv.className = 'stage-date';
                const stageDate = new Date(stage.created_at);
                dateDiv.textContent = stageDate.toLocaleDateString('ru-RU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: '2-digit'
                });
                
                // Тип этапа (цветной лейбл)
                const typeDiv = document.createElement('div');
                typeDiv.className = `stage-type stage-type-${stage.stage_type.toLowerCase()}`;
                typeDiv.textContent = stage.stage_type.toLowerCase();
                
                // Заголовок этапа
                const titleDiv = document.createElement('div');
                titleDiv.className = 'stage-title';
                titleDiv.textContent = stage.title || 'Без названия';
                
                // Описание (если есть)
                const descDiv = document.createElement('div');
                descDiv.className = 'stage-description';
                descDiv.textContent = stage.description || '';
                
                // Кнопка удаления
                const delBtn = document.createElement('button');
                delBtn.className = 'stage-delete-btn';
                delBtn.title = 'Удалить этап';
                delBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>`;
                delBtn.onclick = function(e) {
                    e.stopPropagation();
                    showDeleteStageModal(stage.id, renderStagesBlock);
                };
                
                // Собираем элементы
                stageDiv.appendChild(dateDiv);
                stageDiv.appendChild(typeDiv);
                stageDiv.appendChild(titleDiv);
                stageDiv.appendChild(descDiv);
                stageDiv.appendChild(delBtn);
                stagesBlock.appendChild(stageDiv);
            });
            // + Добавить
            const addRow = document.createElement('div');
            addRow.className = 'stage-add-row';
            const addBtn = document.createElement('span');
            addBtn.className = 'stage-add-btn';
            addBtn.textContent = '+ Добавить этап';
            addRow.appendChild(addBtn);
            stagesBlock.appendChild(addRow);
            // Логика добавления этапа
            addBtn.addEventListener('click', function() {
                showAddStageModal(vacancy, renderStagesBlock);
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

// Базовый компонент модального окна
class Modal {
    constructor({ title = '', content = '', onClose = null, onSubmit = null, submitText = '', cancelText = 'Отмена', showFooter = true }) {
        this.modal = document.createElement('div');
        this.modal.className = 'modal show';
        this.modal.innerHTML = `
            <div class="modal-content modal-base-content">
                <div class="modal-header"><h2>${title}</h2></div>
                <form class="modal-form">${typeof content === 'string' ? content : ''}</form>
            </div>
        `;
        document.body.appendChild(this.modal);
        this.form = this.modal.querySelector('.modal-form');
        if (typeof content !== 'string' && content instanceof HTMLElement) {
            this.form.appendChild(content);
        }
        // Footer с кнопками
        if (showFooter) {
            const footer = document.createElement('div');
            footer.className = 'modal-footer';
            if (submitText) {
                this.submitBtn = document.createElement('button');
                this.submitBtn.type = 'submit';
                this.submitBtn.className = 'btn btn-primary';
                this.submitBtn.textContent = submitText;
                footer.appendChild(this.submitBtn);
            }
            this.cancelBtn = document.createElement('button');
            this.cancelBtn.type = 'button';
            this.cancelBtn.className = 'btn btn-secondary';
            this.cancelBtn.textContent = cancelText;
            this.cancelBtn.onclick = () => this.close();
            footer.appendChild(this.cancelBtn);
            this.form.appendChild(footer);
        }
        // Закрытие по клику вне окна
        this.modal.onclick = (e) => { if (e.target === this.modal) this.close(); };
        // Закрытие по Escape
        this.escListener = (e) => { if (e.key === 'Escape') this.close(); };
        window.addEventListener('keydown', this.escListener);
        // Сабмит
        if (onSubmit) {
            this.form.onsubmit = async (e) => {
                e.preventDefault();
                await onSubmit(this);
            };
        }
        this.onClose = onClose;
    }
    close() {
        window.removeEventListener('keydown', this.escListener);
        this.modal.remove();
        if (this.onClose) this.onClose();
    }
    setContent(htmlOrElement) {
        this.form.innerHTML = '';
        if (typeof htmlOrElement === 'string') {
            this.form.innerHTML = htmlOrElement;
        } else if (htmlOrElement instanceof HTMLElement) {
            this.form.appendChild(htmlOrElement);
        }
    }
}

// Универсальная модалка для добавления/редактирования вакансии
function showVacancyModal({ mode = 'add', vacancy = null }) {
    const isEdit = mode === 'edit';
    const formHtml = `
        <div class="form-group">
            <label>Название</label>
            <input type="text" name="title" class="form-control" required maxlength="100" value="${isEdit && vacancy ? escapeHtml(vacancy.name) : ''}" />
        </div>
        <div class="form-group">
            <label>Ссылка на вакансию</label>
            <input type="url" name="link" class="form-control" maxlength="300" value="${isEdit && vacancy ? escapeHtml(vacancy.link || '') : ''}" />
        </div>
        <div class="form-group">
            <label>Компания</label>
            <input type="text" name="company" class="form-control" maxlength="300" value="${isEdit && vacancy ? escapeHtml(vacancy.company_name || '') : ''}" />

        </div>
        <div class="form-group">
            <label>Описание или комментарий</label>
            <textarea name="description" class="form-control" rows="2" maxlength="300">${isEdit && vacancy ? escapeHtml(vacancy.description || '') : ''}</textarea>
        </div>
    `;
    const modal = new Modal({
        title: isEdit ? 'Редактировать вакансию' : 'Добавить вакансию',
        content: formHtml,
        submitText: isEdit ? 'Сохранить' : 'Добавить',
        cancelText: 'Отмена',
        onSubmit: async (modalInstance) => {
            const form = modalInstance.form;
            const data = {
                name: form.title.value.trim(),
                link: form.link.value.trim(),
                company_name: form.company.value,
                description: form.description.value.trim()
            };
            try {
                let newVacancy;
                if (isEdit && vacancy) {
                    newVacancy = await app.vacancyClient.updateVacancy(vacancy.id, data);
                } else {
                    newVacancy = await app.vacancyClient.createVacancy(data);
                }
                modalInstance.close();
                // Обновить/добавить вакансию в DOM
                const grid = document.querySelector('.vacancies-list-items');
                const renderer = app.vacancyRenderer || new VacancyRenderer();
                if (isEdit && vacancy) {
                    // Найти и заменить карточку
                    const card = grid.querySelector(`[data-vacancy-id="${vacancy.id}"]`);
                    if (card) {
                        const outer = card.closest('.vacancy-card-outer');
                        const newItem = renderer.createVacancyItem(newVacancy);
                        grid.replaceChild(newItem, outer);
                    }
                } else {
                    // Добавить новую карточку первой
                    const newItem = renderer.createVacancyItem(newVacancy);
                    grid.prepend(newItem);
                }
                app.messageManager.showSuccess(isEdit ? 'Вакансия обновлена!' : 'Вакансия добавлена!');
            } catch (err) {
                app.messageManager.showError(isEdit ? 'Ошибка обновления вакансии' : 'Ошибка добавления вакансии');
            }
        }
    });
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

// Для экранирования html в форме
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

// Модальное окно для добавления этапа
function showAddStageModal(vacancy, onSuccess) {
    // Определяем предзаполненный тип этапа
    const lastStage = Array.isArray(vacancy.stages) && vacancy.stages.length > 0 ? vacancy.stages[vacancy.stages.length - 1] : null;
    const currentStageType = lastStage && lastStage.stage_type ? lastStage.stage_type : 'new';
    const defaultStageType = currentStageType === 'new' ? 'hr' : currentStageType;
    
    // Текущая дата в формате YYYY-MM-DD
    const today = new Date().toISOString().split('T')[0];
    
    const formHtml = `
        <div class="form-group">
            <label>Тип этапа</label>
            <select name="stage_type" class="form-control" required>
                <option value="new" ${defaultStageType === 'new' ? 'selected' : ''}>Новая вакансия</option>
                <option value="hr" ${defaultStageType === 'hr' ? 'selected' : ''}>Этап HR</option>
                <option value="tech" ${defaultStageType === 'tech' ? 'selected' : ''}>Технический этап</option>
                <option value="business" ${defaultStageType === 'business' ? 'selected' : ''}>Бизнес этап</option>
                <option value="rejected" ${defaultStageType === 'rejected' ? 'selected' : ''}>Отказ</option>
                <option value="offer" ${defaultStageType === 'offer' ? 'selected' : ''}>Оффер</option>
            </select>
        </div>
        <div class="form-group">
            <label>Дата этапа</label>
            <input type="date" name="date" class="form-control" value="${today}" required>
        </div>
        <div class="form-group">
            <label>Название этапа</label>
            <input type="text" name="title" class="form-control" maxlength="255" placeholder="Название этапа">
            <div class="suggestions-container" style="margin-top: 8px;">
                <div class="suggestions-list" style="display: flex; flex-wrap: wrap; gap: 4px;">
                    <!-- Подсказки будут добавлены динамически -->
                </div>
            </div>
        </div>
        <div class="form-group">
            <label>Описание</label>
            <textarea name="description" class="form-control" rows="3" maxlength="1000" placeholder="Описание этапа"></textarea>
        </div>
    `;
    
    const modal = new Modal({
        title: 'Добавить этап',
        content: formHtml,
        submitText: 'Добавить',
        cancelText: 'Отмена',
        onSubmit: async (modalInstance) => {
            const form = modalInstance.form;
            const data = {
                vacancy_id: vacancy.id,
                stage_type: form.stage_type.value.toUpperCase(),
                title: form.title.value.trim(),
                description: form.description.value.trim()
            };
            
            // Если выбрана дата, добавляем её в формате ISO без timezone
            if (form.date.value) {
                const selectedDate = new Date(form.date.value);
                // Форматируем дату без timezone информации
                const year = selectedDate.getFullYear();
                const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
                const day = String(selectedDate.getDate()).padStart(2, '0');
                data.created_at = `${year}-${month}-${day}T00:00:00`;
            }
            
            try {
                await app.stageClient.createStage(data);
                modalInstance.close();
                if (onSuccess) await onSuccess();
                app.messageManager.showSuccess('Этап добавлен!');
            } catch (err) {
                app.messageManager.showError('Ошибка добавления этапа');
            }
        }
    });
    
    // Добавляем логику для подсказок
    const form = modal.modal.querySelector('form');
    const stageTypeSelect = form.querySelector('select[name="stage_type"]');
    const titleInput = form.querySelector('input[name="title"]');
    const suggestionsList = form.querySelector('.suggestions-list');
    
    // Функция для обновления подсказок
    function updateSuggestions() {
        const selectedStageType = stageTypeSelect.value.toUpperCase();
        const suggestions = STAGE_TITLE_SUGGESTIONS[selectedStageType] || [];
        
        suggestionsList.innerHTML = '';
        suggestions.forEach(suggestion => {
            const suggestionBtn = document.createElement('button');
            suggestionBtn.type = 'button';
            suggestionBtn.className = 'suggestion-btn';
            suggestionBtn.textContent = suggestion;
            suggestionBtn.onclick = () => {
                titleInput.value = suggestion;
                titleInput.focus();
            };
            suggestionsList.appendChild(suggestionBtn);
        });
    }
    
    // Инициализируем подсказки
    updateSuggestions();
    
    // Обновляем подсказки при изменении типа этапа
    stageTypeSelect.addEventListener('change', updateSuggestions);
}


window.showVacancyModal = showVacancyModal;
window.showAddStageModal = showAddStageModal;