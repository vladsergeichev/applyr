// Менеджер сообщений для отображения уведомлений
class MessageManager {
    constructor(containerId = 'message-container') {
        this.container = document.getElementById(containerId);
        this.messageQueue = [];
        this.isProcessing = false;
    }

    // Показывает сообщение
    show(message, type = 'info', duration = 5000) {
        const messageData = {
            id: Date.now() + Math.random(),
            message,
            type,
            duration
        };

        this.messageQueue.push(messageData);
        this.processQueue();
    }

    // Показывает сообщение об успехе
    showSuccess(message, duration = 3000) {
        this.show(message, 'success', duration);
    }

    // Показывает сообщение об ошибке
    showError(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    // Показывает предупреждение
    showWarning(message, duration = 4000) {
        this.show(message, 'warning', duration);
    }

    // Показывает информационное сообщение
    showInfo(message, duration = 3000) {
        this.show(message, 'info', duration);
    }

    // Показывает сообщение о загрузке
    showLoading(message = 'Загрузка...', duration = 0) {
        this.show(message, 'loading', duration);
    }

    // Обрабатывает очередь сообщений
    async processQueue() {
        if (this.isProcessing || this.messageQueue.length === 0) {
            return;
        }

        this.isProcessing = true;

        while (this.messageQueue.length > 0) {
            const messageData = this.messageQueue.shift();
            await this.displayMessage(messageData);
        }

        this.isProcessing = false;
    }

    // Отображает сообщение
    async displayMessage(messageData) {
        const messageElement = this.createMessageElement(messageData);
        messageElement.classList.add('message-slide-in');
        this.container.appendChild(messageElement);

        // Принудительно вызываем reflow
        messageElement.offsetHeight;
        
        // Запускаем анимацию появления
        messageElement.classList.add('show');

        // Автоматическое удаление
        if (messageData.duration > 0) {
            setTimeout(() => {
                this.removeMessage(messageElement);
            }, messageData.duration);
        }
    }

    // Создает элемент сообщения
    createMessageElement(messageData) {
        const messageElement = document.createElement('div');
        messageElement.className = `message message-${messageData.type}`;
        messageElement.id = `message-${messageData.id}`;
        
        const icon = this.getIcon(messageData.type);
        messageElement.innerHTML = `
            <div class="message-content">
                <span class="message-icon">${icon}</span>
                <span class="message-text">${messageData.message}</span>
                <button class="message-close" onclick="this.parentElement.parentElement.remove()">
                    ×
                </button>
            </div>
        `;

        return messageElement;
    }

    // Удаляет сообщение
    async removeMessage(messageElement) {
        if (!messageElement || !messageElement.parentNode) {
            return;
        }

        // Анимация исчезновения - сдвигаем вправо
        messageElement.classList.add('message-slide-out');
        
        // Ждем завершения анимации
        setTimeout(() => {
            messageElement.remove();
        }, 300);
    }

    // Получает иконку для типа сообщения
    getIcon(type) {
        const icons = {
            success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>',
            error: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>',
            warning: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
            loading: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>'
        };
        return icons[type] || icons.info;
    }



    // Очищает все сообщения
    clear() {
        this.messageQueue = [];
        this.container.innerHTML = '';
    }
} 