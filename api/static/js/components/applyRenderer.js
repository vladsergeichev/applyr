// Компонент для рендеринга откликов
class ApplyRenderer {
    constructor(containerId = 'applies-list') {
        this.container = document.getElementById(containerId);
        this.noAppliesContainer = document.getElementById('no-applies');
        this.currentUsername = null;
    }

    // Рендерит список откликов
    render(applies, username) {
        this.currentUsername = username;
        
        if (!applies || applies.length === 0) {
            this.showNoApplies();
            return;
        }

        this.hideNoApplies();
        this.container.innerHTML = this.createAppliesListHTML(applies, username);
        this.attachEventListeners();
    }

    // Создает HTML для списка откликов
    createAppliesListHTML(applies, username) {
        const appliesHTML = applies.map(apply => this.createApplyItemHTML(apply)).join('');
        
        return `
            <div class="applies-header">
                <h3>Отклики пользователя @${username}:</h3>
                <span class="applies-count">${applies.length} откликов</span>
            </div>
            <div class="applies-grid">
                ${appliesHTML}
            </div>
        `;
    }

    // Создает HTML для одного отклика
    createApplyItemHTML(apply) {
        const createdDate = this.formatDate(apply.created_at);
        const escapedName = this.escapeHtml(apply.name);
        
        return `
            <div class="apply-item" id="apply-${apply.id}" data-apply-id="${apply.id}">
                <div class="apply-header">
                    <div class="apply-title">${escapedName}</div>
                    <div class="apply-actions">
                        <button class="delete-btn" data-apply-id="${apply.id}" data-apply-name="${escapedName}">
                            🗑️
                        </button>
                    </div>
                </div>
                <div class="apply-meta">
                    <span class="apply-date">📅 Создан: ${createdDate}</span>
                </div>
                <div class="apply-link-container">
                    <a href="${apply.link}" class="apply-link" target="_blank" rel="noopener noreferrer">
                        🔗 Перейти к вакансии
                    </a>
                </div>
                ${apply.description ? `<div class="apply-description">${this.escapeHtml(apply.description)}</div>` : ''}
            </div>
        `;
    }

    // Форматирует дату

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Экранирует HTML
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Прикрепляет обработчики событий
    attachEventListeners() {
        const deleteButtons = this.container.querySelectorAll('.delete-btn');
        
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const applyId = button.dataset.applyId;
                const applyName = button.dataset.applyName;
                this.handleDelete(applyId, applyName);
            });
        });
    }

    // Обрабатывает удаление отклика
    async handleDelete(applyId, applyName) {
        if (!confirm(`Удалить отклик "${applyName}"?`)) {
            return;
        }

        try {
            // Показываем индикатор загрузки на кнопке
            const button = this.container.querySelector(`[data-apply-id="${applyId}"]`);
            const originalText = button.innerHTML;
            button.innerHTML = '⏳';
            button.disabled = true;

            await applyClient.deleteApply(applyId);
            
            // Удаляем элемент с анимацией
            const applyElement = this.container.querySelector(`#apply-${applyId}`);
            if (applyElement) {
                await this.animateRemove(applyElement);
            }

            messageManager.success('Отклик успешно удален!');
            
            // Обновляем счетчик
            this.updateAppliesCount();
            
        } catch (error) {
            console.error('Ошибка при удалении отклика:', error);
            messageManager.error('Ошибка при удалении отклика');
            
            // Восстанавливаем кнопку
            const button = this.container.querySelector(`[data-apply-id="${applyId}"]`);
            if (button) {
                button.innerHTML = '🗑️';
                button.disabled = false;
            }
        }
    }

    // Анимирует удаление элемента
    async animateRemove(element) {
        element.style.transition = 'all 0.3s ease';
        element.style.opacity = '0';
        element.style.transform = 'scale(0.8)';
        
        await new Promise(resolve => setTimeout(resolve, 300));
        element.remove();
    }

    // Обновляет счетчик откликов
    updateAppliesCount() {
        const countElement = this.container.querySelector('.applies-count');
        const applyItems = this.container.querySelectorAll('.apply-item');
        
        if (countElement) {
            countElement.textContent = `${applyItems.length} откликов`;
        }
    }

    // Показывает сообщение об отсутствии откликов
    showNoApplies() {
        this.container.classList.add('hidden');
        this.noAppliesContainer.classList.remove('hidden');
    }

    // Скрывает сообщение об отсутствии откликов
    hideNoApplies() {
        this.container.classList.remove('hidden');
        this.noAppliesContainer.classList.add('hidden');
    }

    // Очищает контейнер
    clear() {
        this.container.innerHTML = '';
        this.currentUsername = null;
    }

    // Показывает индикатор загрузки
    showLoading() {
        this.container.innerHTML = `
            <div class="loading-applies">
                <div class="spinner"></div>
                <p>Загрузка откликов...</p>
            </div>
        `;
    }

    // Показывает ошибку
    showError(message) {
        this.container.innerHTML = `
            <div class="error-applies">
                <div class="error-icon">❌</div>
                <p>${message}</p>
            </div>
        `;
    }
} 