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
        this.container.appendChild(messageElement);

        // Анимация появления
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateX(100%)';
        
        await this.animate(messageElement, {
            opacity: '1',
            transform: 'translateX(0)'
        }, 300);

        // Автоматическое удаление
        setTimeout(() => {
            this.removeMessage(messageElement);
        }, messageData.duration);
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

        // Анимация исчезновения
        await this.animate(messageElement, {
            opacity: '0',
            transform: 'translateX(100%)'
        }, 300);

        messageElement.remove();
    }

    // Получает иконку для типа сообщения
    getIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️',
            loading: '⏳'
        };
        return icons[type] || icons.info;
    }

    // Анимация CSS свойств
    animate(element, properties, duration = 300) {
        return new Promise(resolve => {
            const startTime = performance.now();
            const startValues = {};
            
            // Получаем начальные значения
            for (const [property, value] of Object.entries(properties)) {
                startValues[property] = parseFloat(getComputedStyle(element)[property]) || 0;
            }

            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Применяем анимацию
                for (const [property, targetValue] of Object.entries(properties)) {
                    const startValue = startValues[property];
                    const currentValue = startValue + (parseFloat(targetValue) - startValue) * progress;
                    element.style[property] = property === 'opacity' ? currentValue : `${currentValue}px`;
                }

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    resolve();
                }
            };

            requestAnimationFrame(animate);
        });
    }

    // Очищает все сообщения
    clear() {
        this.messageQueue = [];
        this.container.innerHTML = '';
    }
} 