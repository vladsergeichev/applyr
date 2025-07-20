// Главное приложение Applyr Dashboard
// Основное приложение
class App {
    constructor() {
        console.log('Инициализация приложения...');

        this.authClient = new AuthClient();
        this.vacancyClient = new VacancyClient();
        this.stageClient = new StageClient();

        this.messageManager = new MessageManager();
        this.vacancyRenderer = new VacancyRenderer();

        this.currentUser = null;
        this.accessToken = localStorage.getItem('accessToken');

        this.initializeApp();
    }

    initializeApp() {
        console.log('Настройка приложения...');
        this.setupEventListeners();
        this.checkAuthStatus();
        console.log('Приложение инициализировано');
    }

    setupEventListeners() {
        console.log('Настройка обработчиков событий...');

        // Кнопки аутентификации
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const logoutBtn = document.getElementById('logout-btn');

        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                console.log('Кнопка входа нажата');
                this.showLoginModal();
            });
        } else {
            console.error('Кнопка входа не найдена');
        }

        if (registerBtn) {
            registerBtn.addEventListener('click', () => {
                console.log('Кнопка регистрации нажата');
                this.showRegisterModal();
            });
        } else {
            console.error('Кнопка регистрации не найдена');
        }

        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Модальные окна
        const closeLoginBtn = document.getElementById('close-login');
        const closeRegisterBtn = document.getElementById('close-register');
        const closeTelegramBtn = document.getElementById('close-telegram');

        if (closeLoginBtn) {
            closeLoginBtn.addEventListener('click', () => this.hideLoginModal());
        }

        if (closeRegisterBtn) {
            closeRegisterBtn.addEventListener('click', () => this.hideRegisterModal());
        }

        if (closeTelegramBtn) {
            closeTelegramBtn.addEventListener('click', () => this.hideTelegramModal());
        }

        // Переключение между модальными окнами
        const switchToRegisterBtn = document.getElementById('switch-to-register');
        const switchToLoginBtn = document.getElementById('switch-to-login');

        if (switchToRegisterBtn) {
            switchToRegisterBtn.addEventListener('click', () => {
                this.hideLoginModal();
                this.showRegisterModal();
            });
        }

        if (switchToLoginBtn) {
            switchToLoginBtn.addEventListener('click', () => {
                this.hideRegisterModal();
                this.showLoginModal();
            });
        }

        // Формы
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const telegramForm = document.getElementById('telegram-form');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        if (telegramForm) {
            telegramForm.addEventListener('submit', (e) => this.handleTelegramConnect(e));
        }

        // Кнопка подключения Telegram
        const connectTelegramBtn = document.getElementById('connect-telegram-btn');
        if (connectTelegramBtn) {
            connectTelegramBtn.addEventListener('click', () => this.showTelegramModal());
        }

        // Кнопка отмены подключения Telegram
        const cancelTelegramBtn = document.getElementById('cancel-telegram');
        if (cancelTelegramBtn) {
            cancelTelegramBtn.addEventListener('click', () => this.hideTelegramModal());
        }

        // Закрытие модальных окон по клику вне их
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideAllModals();
            }
        });

        console.log('Обработчики событий настроены');
    }

    checkAuthStatus() {
        if (this.accessToken) {
            this.authClient.setAuthToken(this.accessToken);
            this.vacancyClient.setAuthToken(this.accessToken);
            this.stageClient.setAuthToken(this.accessToken);

            this.getCurrentUserInfo();
        } else {
            this.showAuthButtons();
        }
    }

    async getUserInfoFromJWT() {
        try {
            return JSON.parse(atob(this.accessToken.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
        } catch (e) {
            return null;
        }
    }

    async getCurrentUserInfo() {
        try {
            const userInfo = await this.getUserInfoFromJWT();
            this.currentUser = userInfo;
            this.showMainContent();
            this.updateUserInfo();
            this.messageManager.showSuccess(`Добро пожаловать, ${userInfo.username}!`);

            // Автоматически загружаем вакансии текущего пользователя
            await this.loadUserVacancies();
        } catch (error) {
            console.error('Ошибка получения информации о пользователе:', error);
            this.logout();
        }
    }

    updateUserInfo() {
        const userInfoElement = document.getElementById('current-user-info');
        if (userInfoElement && this.currentUser) {
            let userText = `Пользователь: ${this.currentUser.username}`;
            if (this.currentUser.telegram_username) {
                userText += ` | Telegram: @${this.currentUser.telegram_username}`;
            }
            userInfoElement.textContent = userText;
        }
    }

    // Загрузка вакансий текущего пользователя
    async loadUserVacancies() {
        if (!this.currentUser) {
            return;
        }

        try {
            this.vacancyRenderer.showLoading();
            const vacancies = await this.vacancyClient.getVacancies();
            this.vacancyRenderer.renderVacancies(vacancies, this.currentUser.username);
        } catch (error) {
            console.error('Ошибка загрузки вакансий:', error);
            this.vacancyRenderer.showError(error.message || 'Ошибка загрузки вакансий');
        }
    }

    showAuthButtons() {
        document.getElementById('login-btn').classList.remove('hidden');
        document.getElementById('register-btn').classList.remove('hidden');
        document.getElementById('logout-btn').classList.add('hidden');
        document.getElementById('main-content').classList.add('hidden');
    }

    showMainContent() {
        document.getElementById('login-btn').classList.add('hidden');
        document.getElementById('register-btn').classList.add('hidden');
        document.getElementById('logout-btn').classList.remove('hidden');
        document.getElementById('main-content').classList.remove('hidden');
    }

    // Модальные окна
    showLoginModal() {
        console.log('Показ модального окна входа');
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно входа не найдено');
        }
    }

    hideLoginModal() {
        console.log('Скрытие модального окна входа');
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.remove('show');
            document.getElementById('login-form').reset();
        }
    }

    showRegisterModal() {
        console.log('Показ модального окна регистрации');
        const modal = document.getElementById('register-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно регистрации не найдено');
        }
    }

    hideRegisterModal() {
        console.log('Скрытие модального окна регистрации');
        const modal = document.getElementById('register-modal');
        if (modal) {
            modal.classList.remove('show');
            document.getElementById('register-form').reset();
        }
    }

    showTelegramModal() {
        console.log('Показ модального окна подключения Telegram');
        const modal = document.getElementById('telegram-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно Telegram не найдено');
        }
    }

    hideTelegramModal() {
        console.log('Скрытие модального окна подключения Telegram');
        const modal = document.getElementById('telegram-modal');
        if (modal) {
            modal.classList.remove('show');
            document.getElementById('telegram-form').reset();
        }
    }

    hideAllModals() {
        this.hideLoginModal();
        this.hideRegisterModal();
        this.hideTelegramModal();
    }

    // Обработка входа
    async handleLogin(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const userData = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        try {
            const response = await this.authClient.login(userData);
            this.accessToken = response.access_token;
            localStorage.setItem('accessToken', this.accessToken);

            this.authClient.setAuthToken(this.accessToken);
            this.vacancyClient.setAuthToken(this.accessToken);
            this.stageClient.setAuthToken(this.accessToken);

            this.hideLoginModal();
            await this.getCurrentUserInfo();
            this.messageManager.showSuccess('Успешный вход в систему!');
        } catch (error) {
            console.error('Ошибка входа:', error);
            this.messageManager.showError(error.message || 'Ошибка входа в систему');
        }
    }

    // Обработка регистрации
    async handleRegister(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const userData = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        try {
            const response = await this.authClient.register(userData);
            this.accessToken = response.access_token;
            localStorage.setItem('accessToken', this.accessToken);

            this.authClient.setAuthToken(this.accessToken);
            this.vacancyClient.setAuthToken(this.accessToken);
            this.stageClient.setAuthToken(this.accessToken);

            this.hideRegisterModal();
            await this.getCurrentUserInfo();
            this.messageManager.showSuccess('Регистрация успешна!');
        } catch (error) {
            console.error('Ошибка регистрации:', error);
            this.messageManager.showError(error.message || 'Ошибка регистрации');
        }
    }

    // Обработка подключения Telegram
    async handleTelegramConnect(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        let telegramUsername = formData.get('telegram_username');

        // Убираем @ если пользователь его ввел
        if (telegramUsername.startsWith('@')) {
            telegramUsername = telegramUsername.substring(1);
        }

        try {
            await this.authClient.updateTelegramUsername({telegram_username: telegramUsername});
            this.hideTelegramModal();

            // Обновляем информацию о пользователе
            await this.getCurrentUserInfo();
            this.messageManager.showSuccess('Telegram успешно подключен!');
        } catch (error) {
            console.error('Ошибка подключения Telegram:', error);
            this.messageManager.showError(error.message || 'Ошибка подключения Telegram');
        }
    }

    // Обновление токенов во всех клиентах
    updateTokens(newAccessToken) {
        this.accessToken = newAccessToken;
        localStorage.setItem('accessToken', this.accessToken);

        this.authClient.setAuthToken(this.accessToken);
        this.vacancyClient.setAuthToken(this.accessToken);
        this.stageClient.setAuthToken(this.accessToken);

        console.log('Токены обновлены во всех клиентах');
    }

    // Выход
    async logout() {
        try {
            await this.authClient.logout();
        } catch (error) {
            console.error('Ошибка выхода:', error);
        } finally {
            this.accessToken = null;
            this.currentUser = null;
            localStorage.removeItem('accessToken');

            this.authClient.clearAuthToken();
            this.vacancyClient.clearAuthToken();
            this.stageClient.clearAuthToken();

            this.showAuthButtons();
            this.vacancyRenderer.clear();
            this.messageManager.showInfo('Вы вышли из системы');
        }
    }
}

// Глобальные функции для кнопок в карточках
function deleteVacancy(vacancyId) {
    if (confirm('Вы уверены, что хотите удалить эту вакансию?')) {
        app.vacancyClient.deleteVacancy(vacancyId)
            .then(() => {
                app.messageManager.showSuccess('Вакансия удалена');
                // Перезагружаем вакансии текущего пользователя
                app.loadUserVacancies();
            })
            .catch(error => {
                console.error('Ошибка удаления вакансии:', error);
                app.messageManager.showError(error.message || 'Ошибка удаления вакансии');
            });
    }
}

// Инициализация приложения
console.log('Загрузка приложения...');
const app = new App(); 