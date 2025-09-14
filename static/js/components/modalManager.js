// Менеджер модальных окон
class ModalManager {
    constructor() {
        this.activeModals = new Set();
    }

    // Создание простого модального окна подтверждения
    createConfirmModal({ title, message, confirmText = 'Подтвердить', cancelText = 'Отмена', onConfirm, onCancel }) {
        const modalId = `modal-${Date.now()}`;
        
        const modal = document.createElement('div');
        modal.className = 'modal show';
        modal.id = modalId;
        modal.innerHTML = `
            <div class="modal-content modal-content-confirm">
                <div class="modal-header"><h2>${title}</h2></div>
                <div class="modal-body modal-body-confirm">${message}</div>
                <div class="modal-footer modal-footer-confirm">
                    <button class="btn btn-danger" id="confirm-${modalId}">${confirmText}</button>
                    <button class="btn btn-secondary" id="cancel-${modalId}">${cancelText}</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.activeModals.add(modalId);

        // Обработчики событий
        const confirmBtn = document.getElementById(`confirm-${modalId}`);
        const cancelBtn = document.getElementById(`cancel-${modalId}`);

        confirmBtn.onclick = () => {
            if (onConfirm) onConfirm();
            this.closeModal(modalId);
        };

        cancelBtn.onclick = () => {
            if (onCancel) onCancel();
            this.closeModal(modalId);
        };

        modal.onclick = (e) => {
            if (e.target === modal) {
                if (onCancel) onCancel();
                this.closeModal(modalId);
            }
        };

        return modalId;
    }

    // Создание модального окна с формой
    createFormModal({ title, formContent, onSubmit, onCancel }) {
        const modalId = `modal-${Date.now()}`;
        
        const modal = document.createElement('div');
        modal.className = 'modal show';
        modal.id = modalId;
        
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${title}</h2>
                </div>
                <form id="form-${modalId}">
                    ${formContent}
                </form>
            </div>
        `;

        document.body.appendChild(modal);
        this.activeModals.add(modalId);

        const form = document.getElementById(`form-${modalId}`);
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            onSubmit(e, modalId);
        });

        modal.onclick = (e) => {
            if (e.target === modal) {
                if (onCancel) onCancel();
                this.closeModal(modalId);
            }
        };

        return modalId;
    }

    // Закрытие модального окна
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.remove();
            this.activeModals.delete(modalId);
        }
    }

    // Закрытие всех модальных окон
    closeAllModals() {
        this.activeModals.forEach(modalId => {
            this.closeModal(modalId);
        });
    }

    // Проверка существования модального окна
    modalExists(modalId) {
        return document.getElementById(modalId) !== null;
    }
}

// Создаем глобальный экземпляр
const modalManager = new ModalManager();

// Экспортируем для использования в других файлах
window.modalManager = modalManager; 