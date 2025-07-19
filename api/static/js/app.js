/**
 * Главное приложение Applyr Dashboard
 */
class App {
    constructor() {
        this.messageManager = null;
        this.applyRenderer = null;
        this.userClient = null;
        this.applyClient = null;
        this.currentUsername = null;
        this.isLoading = false;
    }

    // Инициализирует приложение
    init() {
        this.initializeComponents();
        this.attachEventListeners();
        this.loadFromURL();
    }

    // Инициализирует компоненты
    initializeComponents() {
        // Инициализируем менеджер сообщений
        this.messageManager = new MessageManager();
        
        // Инициализируем рендерер откликов
        this.applyRenderer = new ApplyRenderer();
        
        // Инициализируем API клиенты
        this.userClient = new UserClient();
        this.applyClient = new ApplyClient();
    }

    // Прикрепляет обработчики событий
    attachEventListeners() {
        // Обработчик поиска
        const searchBtn = document.getElementById('search-btn');
        const usernameInput = document.getElementById('username-input');

        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.handleSearch());
        }

        if (usernameInput) {
            // Поиск по Enter
            usernameInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleSearch();
                }
            });
        }
    }

    // Обрабатывает поиск откликов

    async handleSearch() {
        const username = DomUtils.getInputValue('#username-input');
        
        if (DomUtils.isInputEmpty('#username-input')) {
            this.messageManager.warning('Введите username пользователя');
            return;
        }

        if (this.isLoading) {
            return;
        }

        await this.searchApplies(username);
    }

    // Выполняет поиск откликов
    async searchApplies(username) {
        try {
            this.setLoading(true);
            this.currentUsername = username;
            
            // Обновляем URL
            this.updateURL(username);
            
            // Показываем индикатор загрузки
            this.applyRenderer.showLoading();
            DomUtils.show('#loading-spinner');
            
            // Получаем отклики
            const applies = await this.applyClient.getApplies(username);
            
            // Рендерим результат
            this.applyRenderer.render(applies, username);
            
            this.messageManager.success(`Найдено ${applies.length} откликов для @${username}`);
            
        } catch (error) {
            console.error('Ошибка при поиске откликов:', error);
            
            if (error.message.includes('не найден')) {
                this.applyRenderer.showError(`Пользователь @${username} не найден`);
                this.messageManager.error(`Пользователь @${username} не найден`);
            } else {
                this.applyRenderer.showError('Ошибка при загрузке откликов');
                this.messageManager.error('Ошибка при загрузке откликов');
            }
        } finally {
            this.setLoading(false);
            DomUtils.hide('#loading-spinner');
        }
    }

    // Устанавливает состояние загрузки
    setLoading(loading) {
        this.isLoading = loading;
        const searchBtn = document.getElementById('search-btn');
        const usernameInput = document.getElementById('username-input');
        
        if (searchBtn) {
            searchBtn.disabled = loading;
            searchBtn.textContent = loading ? 'Поиск...' : 'Показать отклики';
        }
        
        if (usernameInput) {
            usernameInput.disabled = loading;
        }
    }

    // Обновляет URL с параметрами
    updateURL(username) {
        const url = new URL(window.location);
        if (username) {
            url.searchParams.set('username', username);
        } else {
            url.searchParams.delete('username');
        }
        window.history.pushState({}, '', url);
    }

    // Загружает данные из URL при загрузке страницы
    loadFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get('username');
        
        if (username) {
            DomUtils.setInputValue('#username-input', username);
            this.searchApplies(username);
        }
    }

    // Очищает результаты поиска
    clearResults() {
        this.applyRenderer.clear();
        this.currentUsername = null;
        this.updateURL('');
        DomUtils.clearInput('#username-input');
    }

    // Обновляет отклики для текущего пользователя
    async refreshApplies() {
        if (this.currentUsername) {
            await this.searchApplies(this.currentUsername);
        }
    }
}

// Глобальные экземпляры для доступа из других компонентов
let messageManager;
let applyClient;
let userClient;

// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.init();
    
    // Делаем компоненты доступными глобально
    messageManager = app.messageManager;
    applyClient = app.applyClient;
    userClient = app.userClient;
    
    console.log('Applyr Dashboard инициализирован');
}); 