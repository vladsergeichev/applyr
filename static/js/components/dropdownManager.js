// Базовый компонент дропдауна
class Dropdown {
    constructor({
        triggerButton = null,
        items = [],
        containerClass = 'user-profile',
        menuClass = 'profile-dropdown',
        itemClass = 'profile-dropdown-item',
        onShow = null,
        onHide = null
    }) {
        this.container = document.createElement('div');
        this.container.className = containerClass;
        this.onShow = onShow;
        this.onHide = onHide;

        // Если кнопка не передана, создаем дефолтную
        if (!triggerButton) {
            this.triggerButton = document.createElement('button');
            this.triggerButton.className = 'action-btn';
            this.triggerButton.title = 'Действия';
            this.triggerButton.innerHTML = Icons.threeDots;
        } else {
            this.triggerButton = triggerButton;
        }

        // Создаем меню
        this.menu = document.createElement('div');
        this.menu.className = menuClass;

        // Добавляем пункты меню
        items.forEach(item => {
            const menuItem = document.createElement('a');
            menuItem.href = '#';
            menuItem.className = itemClass + (item.className ? ` ${item.className}` : '');
            menuItem.textContent = item.text;
            
            menuItem.onclick = async (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.hide();
                if (item.onClick) {
                    await item.onClick(e);
                }
            };

            this.menu.appendChild(menuItem);
        });

        // Собираем дропдаун
        this.container.appendChild(this.triggerButton);
        this.container.appendChild(this.menu);

        this.setupEventListeners();
    }

    setupEventListeners() {
        // Открытие/закрытие по клику на кнопку
        this.triggerButton.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        };

        // Закрытие при клике вне дропдауна
        this.closeHandler = (e) => {
            if (!this.container.contains(e.target)) {
                this.hide();
            }
        };

        // Закрытие при нажатии Escape
        this.escHandler = (e) => {
            if (e.key === 'Escape') {
                this.hide();
            }
        };
    }

    show() {
        this.menu.classList.add('show');
        document.addEventListener('click', this.closeHandler);
        document.addEventListener('keydown', this.escHandler);
        if (this.onShow) this.onShow();
    }

    hide() {
        this.menu.classList.remove('show');
        document.removeEventListener('click', this.closeHandler);
        document.removeEventListener('keydown', this.escHandler);
        if (this.onHide) this.onHide();
    }

    toggle() {
        if (this.menu.classList.contains('show')) {
            this.hide();
        } else {
            this.show();
        }
    }

    getContainer() {
        return this.container;
    }
}

// Экспорт в глобальную область
window.Dropdown = Dropdown;
