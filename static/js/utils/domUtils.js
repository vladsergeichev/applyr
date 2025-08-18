// Утилиты для работы с DOM
class DomUtils {
    // Показывает элемент
    static show(element) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.remove('hidden');
        }
    }

    // Скрывает элемент
    static hide(element) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.add('hidden');
        }
    }

    // Переключает видимость элемента
    static toggle(element) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.toggle('hidden');
        }
    }

    // Проверяет, скрыт ли элемент
    static isHidden(element) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        return el ? el.classList.contains('hidden') : true;
    }

    // Получает значение поля ввода
    static getInputValue(selector) {
        const input = document.querySelector(selector);
        return input ? input.value.trim() : '';
    }

    // Устанавливает значение поля ввода
    static setInputValue(selector, value) {
        const input = document.querySelector(selector);
        if (input) {
            input.value = value;
        }
    }

    // Очищает поле ввода
    static clearInput(selector) {
        this.setInputValue(selector, '');
    }

    // Проверяет, пустое ли поле ввода
    static isInputEmpty(selector) {
        return this.getInputValue(selector) === '';
    }

    // Добавляет класс к элементу
    static addClass(element, className) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.add(className);
        }
    }

    // Удаляет класс у элемента
    static removeClass(element, className) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.remove(className);
        }
    }

    // Переключает класс у элемента
    static toggleClass(element, className) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.classList.toggle(className);
        }
    }

    // Проверяет, содержит ли элемент класс
    static hasClass(element, className) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        return el ? el.classList.contains(className) : false;
    }

    // Создает элемент с атрибутами
    static createElement(tagName, attributes = {}, textContent = '') {
        const element = document.createElement(tagName);
        
        // Устанавливаем атрибуты
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'textContent') {
                element.textContent = value;
            } else {
                element.setAttribute(key, value);
            }
        });

        // Устанавливаем текстовое содержимое
        if (textContent) {
            element.textContent = textContent;
        }

        return element;
    }

    // Добавляет обработчик события с делегированием
    static delegate(parent, selector, event, handler) {
        const parentElement = typeof parent === 'string' ? document.querySelector(parent) : parent;
        if (parentElement) {
            parentElement.addEventListener(event, (e) => {
                const target = e.target.closest(selector);
                if (target && parentElement.contains(target)) {
                    handler.call(target, e);
                }
            });
        }
    }

    // Анимирует появление элемента
    static async fadeIn(element, duration = 300) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (!el) return;

        el.classList.add('fade-in-animation');
        this.show(el);

        await new Promise(resolve => setTimeout(resolve, 10));
        el.classList.add('show');

        return new Promise(resolve => {
            setTimeout(resolve, duration);
        });
    }

    // Анимирует исчезновение элемента
    static async fadeOut(element, duration = 300) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (!el) return;

        el.classList.add('fade-out-animation');
        el.classList.add('hide');

        return new Promise(resolve => {
            setTimeout(() => {
                this.hide(el);
                el.classList.remove('fade-out-animation', 'hide');
                resolve();
            }, duration);
        });
    }

    // Прокручивает к элементу
    static scrollTo(element, options = {}) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (el) {
            el.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
                ...options
            });
        }
    }

    // Копирует текст в буфер обмена
    static async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            console.error('Ошибка копирования в буфер обмена:', error);
            return false;
        }
    }
} 