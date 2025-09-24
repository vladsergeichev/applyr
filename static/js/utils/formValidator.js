// Валидатор форм
class FormValidator {
    constructor() {
        this.errorMessages = {
            required: 'Это поле обязательно для заполнения',
            minLength: (min) => `Минимум ${min} символов`,
            maxLength: (max) => `Максимум ${max} символов`,
            email: 'Введите корректный email',
            passwordMatch: 'Пароли не совпадают',
            url: 'Введите корректный URL'
        };
    }

    // Валидация регистрации
    validateRegisterForm(userData) {
        const errors = {};

        // Валидация username
        if (!userData.username || userData.username.trim().length < 3) {
            errors.username = this.errorMessages.minLength(3);
        }

        // Валидация пароля
        if (!userData.password || userData.password.length < 6) {
            errors.password = this.errorMessages.minLength(6);
        }

        // Валидация подтверждения пароля
        if (userData.password !== userData.password_confirm) {
            errors.password_confirm = this.errorMessages.passwordMatch;
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    // Валидация входа
    validateLoginForm(userData) {
        const errors = {};

        if (!userData.username || !userData.username.trim()) {
            errors.username = this.errorMessages.required;
        }

        if (!userData.password || !userData.password.trim()) {
            errors.password = this.errorMessages.required;
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    // Валидация вакансии
    validateVacancyForm(vacancyData) {
        const errors = {};

        if (!vacancyData.name || !vacancyData.name.trim()) {
            errors.name = this.errorMessages.required;
        }

        if (vacancyData.link && !this.isValidUrl(vacancyData.link)) {
            errors.link = this.errorMessages.url;
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    // Проверка URL
    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    // Показать ошибки в форме
    showFormErrors(form, errors) {
        // Очищаем предыдущие ошибки
        this.clearFormErrors(form);

        // Показываем новые ошибки
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            const errorElement = form.querySelector(`#${fieldName}-error`);
            
            if (field) {
                field.classList.add('error');
            }
            
            if (errorElement) {
                errorElement.textContent = errors[fieldName];
                errorElement.classList.add('show');
            }
        });
    }

    // Очистить ошибки формы
    clearFormErrors(form) {
        const errorElements = form.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.classList.remove('show');
            element.textContent = '';
        });

        const fields = form.querySelectorAll('input, textarea, select');
        fields.forEach(field => {
            field.classList.remove('error');
        });
    }

    // Подсветить поле с ошибкой
    highlightField(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.add('error');
        }
    }

    // Очистить ошибку конкретного поля
    clearFieldError(fieldName) {
        const field = document.querySelector(`[name="${fieldName}"]`);
        const errorElement = document.querySelector(`#${fieldName}-error`);
        
        if (field) {
            field.classList.remove('error');
        }
        
        if (errorElement) {
            errorElement.classList.remove('show');
            errorElement.textContent = '';
        }
    }
}

// Создаем глобальный экземпляр
const formValidator = new FormValidator();

// Экспортируем для использования в других файлах
window.formValidator = formValidator; 