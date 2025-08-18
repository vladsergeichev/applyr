// Используем константы из отдельного файла

// Утилиты
const Utils = {
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    },

    formatDate(date) {
        return new Date(date).toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: '2-digit'
        });
    },

    getLastStage(vacancy) {
        return Array.isArray(vacancy.stages) && vacancy.stages.length > 0 
            ? vacancy.stages[vacancy.stages.length - 1] 
            : null;
    }
};

// Иконки SVG
const Icons = {
    edit: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>`,
    delete: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>`,
    link: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
    deleteSmall: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>`
};

// Рендерер для отображения вакансий
class VacancyRenderer {
    constructor() {
        this.vacanciesList = document.getElementById('vacancies-list');
    }

    clear() {
        this.vacanciesList.innerHTML = '';
        this.vacanciesList.classList.add('hidden');
    }

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

    renderVacancies(vacancies) {
        this.clear();
        const header = this.createVacanciesHeader(vacancies.length);
        const grid = this.createVacanciesGrid(vacancies);
        this.vacanciesList.appendChild(header);
        this.vacanciesList.appendChild(grid);
        this.vacanciesList.classList.remove('hidden');
    }

    createVacanciesHeader(vacanciesLength) {
        const header = document.createElement('div');
        header.className = 'vacancies-header';
        header.innerHTML = `
            <h3>Мои вакансии</h3>
            <span class="vacancies-count-simple">${vacanciesLength}</span>
            <button class="btn btn-primary add-vacancy-btn">+ Добавить вакансию</button>
        `;
        header.querySelector('.add-vacancy-btn').onclick = () => showVacancyModal({ mode: 'add' });
        return header;
    }

    createVacanciesGrid(vacancies) {
        const grid = document.createElement('div');
        grid.className = 'vacancies-list-items vacancies-list-items--fullwidth';
        vacancies.forEach(vacancy => {
            const vacancyItem = this.createVacancyItem(vacancy);
            grid.appendChild(vacancyItem);
        });
        return grid;
    }

    createVacancyItem(vacancy) {
        const outer = document.createElement('div');
        outer.className = 'vacancy-card-outer';

        const item = document.createElement('div');
        item.className = 'vacancy-item';
        item.dataset.vacancyId = vacancy.id;

        // Создаем статус
        const lastStage = Utils.getLastStage(vacancy);
        const status = lastStage?.stage_type || 'new';
        const statusLabel = `<span class="vacancy-status-label vacancy-status-${status}">${Utils.escapeHtml(status)}</span>`;

        // Создаем контент
        const title = `<span class="vacancy-title">${Utils.escapeHtml(vacancy.name)}</span>`;
        const company = `<span class="vacancy-company">${Utils.escapeHtml(vacancy.company_name || '<название компании>')}</span>`;

        // Создаем кнопки действий
        const actionButtons = this.createActionButtons(vacancy);

        item.innerHTML = `
            <div class="vacancy-card-layout">
                <div class="vacancy-card-left">${statusLabel}</div>
                <div class="vacancy-card-center">${title}${company}</div>
                <div class="vacancy-card-right"></div>
            </div>
        `;

        const right = item.querySelector('.vacancy-card-right');
        actionButtons.forEach(btn => right.appendChild(btn));

        // Добавляем функциональность этапов
        this.addStagesFunctionality(item, outer, vacancy);

        outer.appendChild(item);
        return outer;
    }

    createActionButtons(vacancy) {
        const buttons = [];

        // Кнопка ссылки
        if (vacancy.link) {
            const linkBtn = document.createElement('a');
            linkBtn.href = vacancy.link;
            linkBtn.target = '_blank';
            linkBtn.className = 'vacancy-action-btn vacancy-link-btn';
            linkBtn.title = 'Открыть вакансию';
            linkBtn.innerHTML = Icons.link;
            buttons.push(linkBtn);
        }

        // Кнопка редактирования
        const editBtn = document.createElement('button');
        editBtn.className = 'vacancy-action-btn vacancy-edit-btn';
        editBtn.title = 'Редактировать';
        editBtn.innerHTML = Icons.edit;
        editBtn.onclick = (e) => {
            e.stopPropagation();
            window.showVacancyModal({mode: 'edit', vacancy});
        };
        buttons.push(editBtn);

        // Кнопка удаления
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'vacancy-action-btn delete-btn';
        deleteBtn.title = 'Удалить вакансию';
        deleteBtn.innerHTML = Icons.delete;
        deleteBtn.onclick = (e) => { 
            e.stopPropagation(); 
            showDeleteVacancyModal(vacancy.id); 
        };
        buttons.push(deleteBtn);

        return buttons;
    }

    addStagesFunctionality(item, outer, vacancy) {
        const renderStagesBlock = async () => {
            document.querySelectorAll('.vacancy-stages-block').forEach(el => el.remove());
            
            let stages = [];
            try {
                stages = await app.stageClient.getStages(vacancy.id);
            } catch (err) {
                app.messageManager.showError('Ошибка загрузки этапов');
            }

            const stagesBlock = this.createStagesBlock(stages, vacancy, renderStagesBlock);
            outer.appendChild(stagesBlock);
        };

        item.addEventListener('click', function(e) {
            if (e.target.closest('.vacancy-action-btn')) return;
            const next = outer.querySelector('.vacancy-stages-block');
            if (next) { 
                next.remove(); 
                return; 
            }
            renderStagesBlock();
        });
    }

    createStagesBlock(stages, vacancy, onSuccess) {
        const stagesBlock = document.createElement('div');
        stagesBlock.className = 'vacancy-stages-block';

        // Создаем этапы
        (stages || []).forEach(stage => {
            const stageDiv = this.createStageItem(stage, onSuccess);
            stagesBlock.appendChild(stageDiv);
        });

        // Добавляем кнопку добавления
        const addRow = this.createAddStageRow(vacancy, onSuccess);
        stagesBlock.appendChild(addRow);

        return stagesBlock;
    }

    createStageItem(stage, onSuccess) {
        const stageDiv = document.createElement('div');
        stageDiv.className = 'stage-item';
        
        // Дата
        const dateDiv = document.createElement('div');
        dateDiv.className = 'stage-date';
        dateDiv.textContent = Utils.formatDate(stage.created_at);
        
        // Тип этапа
        const typeDiv = document.createElement('div');
        typeDiv.className = `stage-type stage-type-${stage.stage_type.toLowerCase()}`;
        typeDiv.textContent = stage.stage_type.toLowerCase();
        
        // Заголовок
        const titleDiv = document.createElement('div');
        titleDiv.className = 'stage-title';
        titleDiv.textContent = stage.title || 'Без названия';
        
        // Описание
        const descDiv = document.createElement('div');
        descDiv.className = 'stage-description';
        descDiv.textContent = stage.description || '';
        
        // Кнопка удаления
        const delBtn = document.createElement('button');
        delBtn.className = 'stage-delete-btn';
        delBtn.title = 'Удалить этап';
        delBtn.innerHTML = Icons.deleteSmall;
        delBtn.onclick = (e) => {
            e.stopPropagation();
            showDeleteStageModal(stage.id, onSuccess);
        };
        
        // Собираем элементы
        [dateDiv, typeDiv, titleDiv, descDiv, delBtn].forEach(el => stageDiv.appendChild(el));
        
        return stageDiv;
    }

    createAddStageRow(vacancy, onSuccess) {
        const addRow = document.createElement('div');
        addRow.className = 'stage-add-row';
        
        const addBtn = document.createElement('span');
        addBtn.className = 'stage-add-btn';
        addBtn.textContent = '+ Добавить этап';
        addBtn.addEventListener('click', () => showAddStageModal(vacancy, onSuccess));
        
        addRow.appendChild(addBtn);
        return addRow;
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

        this.onSubmit = onSubmit;
        this.onClose = onClose;

        this.setupFooter(showFooter, submitText, cancelText, onSubmit);
        this.setupEventListeners(onClose);
    }

    setupFooter(showFooter, submitText, cancelText, onSubmit) {
        if (!showFooter) return;

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

    setupEventListeners(onClose) {
        this.modal.onclick = (e) => { 
            if (e.target === this.modal) this.close(); 
        };
        
        this.escListener = (e) => { 
            if (e.key === 'Escape') this.close(); 
        };
        window.addEventListener('keydown', this.escListener);
        
        if (this.onSubmit) {
            this.form.onsubmit = async (e) => {
                e.preventDefault();
                await this.onSubmit(this);
            };
        }
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

// Модальные окна
function showVacancyModal({ mode = 'add', vacancy = null }) {
    const isEdit = mode === 'edit';
    const formHtml = `
        <div class="form-group">
            <label>Название</label>
            <input type="text" name="title" class="form-control" required maxlength="100" value="${isEdit && vacancy ? Utils.escapeHtml(vacancy.name) : ''}" />
        </div>
        <div class="form-group">
            <label>Ссылка на вакансию</label>
            <input type="url" name="link" class="form-control" maxlength="300" value="${isEdit && vacancy ? Utils.escapeHtml(vacancy.link || '') : ''}" />
        </div>
        <div class="form-group">
            <label>Компания</label>
            <input type="text" name="company" class="form-control" maxlength="300" value="${isEdit && vacancy ? Utils.escapeHtml(vacancy.company_name || '') : ''}" />
        </div>
        <div class="form-group">
            <label>Описание или комментарий</label>
            <textarea name="description" class="form-control" rows="2" maxlength="300">${isEdit && vacancy ? Utils.escapeHtml(vacancy.description || '') : ''}</textarea>
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
                    newVacancy = await window.app.vacancyClient.updateVacancy(vacancy.id, data);
                } else {
                    newVacancy = await window.app.vacancyClient.createVacancy(data);
                }
                
                modalInstance.close();
                updateVacancyInDOM(isEdit, vacancy, newVacancy);
                window.app.messageManager.showSuccess(isEdit ? 'Вакансия обновлена!' : 'Вакансия добавлена!');
            } catch (err) {
                window.app.messageManager.showError(isEdit ? 'Ошибка обновления вакансии' : 'Ошибка добавления вакансии');
            }
        }
    });
}

function updateVacancyInDOM(isEdit, oldVacancy, newVacancy) {
    const grid = document.querySelector('.vacancies-list-items');
    const renderer = window.app.vacancyRenderer || new VacancyRenderer();
    
    if (isEdit && oldVacancy) {
        const card = grid.querySelector(`[data-vacancy-id="${oldVacancy.id}"]`);
        if (card) {
            const outer = card.closest('.vacancy-card-outer');
            const newItem = renderer.createVacancyItem(newVacancy);
            grid.replaceChild(newItem, outer);
        }
    } else {
        const newItem = renderer.createVacancyItem(newVacancy);
        grid.prepend(newItem);
    }
}

function showDeleteStageModal(stageId, onSuccess) {
    window.modalManager.createConfirmModal({
        title: 'Удалить этап?',
        message: 'Вы уверены, что хотите удалить этап?',
        confirmText: 'Удалить',
        cancelText: 'Отмена',
        onConfirm: async () => {
            try {
                await app.stageClient.deleteStage(stageId);
                if (onSuccess) await onSuccess();
            } catch (err) {
                app.messageManager.showError('Ошибка удаления этапа');
            }
        }
    });
}

function showAddStageModal(vacancy, onSuccess) {
    const lastStage = Utils.getLastStage(vacancy);
    const currentStageType = lastStage?.stage_type || 'new';
    const defaultStageType = currentStageType === 'new' ? 'hr' : currentStageType;
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
            <div class="suggestions-container">
                <div class="suggestions-list">
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
            
            if (form.date.value) {
                const selectedDate = new Date(form.date.value);
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
    
    setupStageSuggestions(modal);
}

function setupStageSuggestions(modal) {
    const form = modal.modal.querySelector('form');
    const stageTypeSelect = form.querySelector('select[name="stage_type"]');
    const titleInput = form.querySelector('input[name="title"]');
    const suggestionsList = form.querySelector('.suggestions-list');
    
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
    
    updateSuggestions();
    stageTypeSelect.addEventListener('change', updateSuggestions);
}

// Экспорт в глобальную область
window.showVacancyModal = showVacancyModal;
window.showAddStageModal = showAddStageModal;