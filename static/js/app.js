// Главное приложение Applyr Dashboard
// Основное приложение
class App {
    constructor() {

        // Используем ApiManager для централизованного управления клиентами
        this.apiManager = new ApiManager();
        this.authClient = this.apiManager.authClient;
        this.vacancyClient = this.apiManager.vacancyClient;
        this.stageClient = this.apiManager.stageClient;

        this.messageManager = new MessageManager();
        this.vacancyRenderer = new VacancyRenderer();

        this.currentUser = null;
        this.accessToken = null; // Убираем localStorage

        this.initializeApp();
    }

    initializeApp() {
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // Кнопка входа
        const loginBtn = document.getElementById('login-btn');
        loginBtn.addEventListener('click', () => this.showLoginModal());

        // Кнопка выхода
        const logoutBtn = document.getElementById('logout-btn');
        logoutBtn.addEventListener('click', () => this.manualLogout());

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

        // --- Формы ---
        // Форма входа
        const loginForm = document.getElementById('login-form');
        loginForm.addEventListener('submit', (e) => this.handleLogin(e));

        // Форма регистрации
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
            
            // Очистка ошибок при вводе
            const registerInputs = registerForm.querySelectorAll('input');
            registerInputs.forEach(input => {
                input.addEventListener('input', () => {
                    input.classList.remove('error');
                    const errorId = input.id.replace('register-', '') + '-error';
                    const errorElement = document.getElementById(errorId);
                    if (errorElement) {
                        errorElement.classList.remove('show');
                    }
                });
            });
        }

        // Форма подключения Telegram
        const telegramForm = document.getElementById('telegram-form');
        telegramForm.addEventListener('submit', (e) => this.handleTelegramConnect(e));

        // Кнопка отмены подключения Telegram
        const cancelTelegramBtn = document.getElementById('cancel-telegram');
        cancelTelegramBtn.addEventListener('click', () => this.hideTelegramModal());

        // Закрытие модальных окон по клику вне их
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideAllModals();
            }
        });
    }

    checkAuthStatus() {
        // Пытаемся получить access_token через refresh_token
        this.tryRefreshToken();
    }

    // Попытка обновления токена при загрузке страницы
    async tryRefreshToken() {
        try {
            const response = await this.authClient.refreshToken();
            
            // Если успешно получили новый токен
            this.accessToken = response.access_token;
            this.apiManager.setAuthToken(this.accessToken);
            
            // Получаем информацию о пользователе без приветственного сообщения
            await this.getCurrentUserInfo(false);
            
        } catch (error) {
            // Показываем кнопку входа если refresh не удался
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

    async getCurrentUserInfo(showWelcomeMessage = true) {
        try {
            const userInfo = await this.getUserInfoFromJWT();
            this.currentUser = userInfo;
            this.showMainContent();
            this.updateUserInfo();
            
            if (showWelcomeMessage) {
                this.messageManager.showSuccess(`Добро пожаловать, ${userInfo.username}!`);
            }

            // Автоматически загружаем вакансии текущего пользователя
            await this.loadUserVacancies();
        } catch (error) {
            console.error('Ошибка получения информации о пользователе:', error);
            // При ошибке - выходим из системы
            this.logout();
        }
    }

    updateUserInfo() {
        const userInfoElement = document.getElementById('current-user-info');
        const telegramStatusElement = document.getElementById('telegram-status');
        
        if (userInfoElement && this.currentUser) {
            userInfoElement.textContent = this.currentUser.username;
        }
        
        if (telegramStatusElement && this.currentUser) {
            if (this.currentUser.telegram_username) {
                // Показываем синюю галочку если Telegram подключен
                telegramStatusElement.innerHTML = `
                    <div class="telegram-connected" title="Telegram подключен. Ваш логин: @${this.currentUser.telegram_username}">
                        <svg class="telegram-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M9 12l2 2 4-4"/>
                        </svg>
                    </div>
                `;
            } else {
                // Показываем кнопку подключения если Telegram не подключен
                telegramStatusElement.innerHTML = `
                    <button id="connect-telegram-btn" class="btn btn-secondary">Подключить Telegram</button>
                `;
                
                // Добавляем обработчик для новой кнопки
                const connectBtn = document.getElementById('connect-telegram-btn');
                if (connectBtn) {
                    connectBtn.addEventListener('click', () => this.showTelegramModal());
                }
            }
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
            this.vacancyRenderer.renderVacancies(vacancies);
        } catch (error) {
            console.error('Ошибка загрузки вакансий:', error);
            this.vacancyRenderer.showError(error.message || 'Ошибка загрузки вакансий');
        }
    }

    showAuthButtons() {
        document.getElementById('login-btn').classList.remove('hidden');
        document.getElementById('user-info').classList.add('hidden');
        document.getElementById('main-content').classList.add('hidden');
    }

    showMainContent() {
        document.getElementById('login-btn').classList.add('hidden');
        document.getElementById('user-info').classList.remove('hidden');
        document.getElementById('main-content').classList.remove('hidden');
    }

    // Модальные окна
    showLoginModal() {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно входа не найдено');
        }
    }

    hideLoginModal() {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.remove('show');
            document.getElementById('login-form').reset();
        }
    }

    showRegisterModal() {
        const modal = document.getElementById('register-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно регистрации не найдено');
        }
    }

    hideRegisterModal() {
        const modal = document.getElementById('register-modal');
        if (modal) {
            modal.classList.remove('show');
            document.getElementById('register-form').reset();
        }
    }

    showTelegramModal() {
        const modal = document.getElementById('telegram-modal');
        if (modal) {
            modal.classList.add('show');
        } else {
            console.error('Модальное окно Telegram не найдено');
        }
    }

    hideTelegramModal() {
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
            this.messageManager.showLoading('Выполняется вход...');
            const response = await this.authClient.login(userData);

            this.accessToken = response.access_token;

            // Используем ApiManager для установки токена всем клиентам
            this.apiManager.setAuthToken(this.accessToken);
            
            this.hideLoginModal();
            this.messageManager.showSuccess('Вход выполнен успешно!');
            
            await this.getCurrentUserInfo();
        } catch (error) {
            console.error('Ошибка входа:', error);
            this.messageManager.showError(error.message || 'Ошибка входа');
        }
    }

    // Обработка регистрации
    async handleRegister(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const userData = {
            username: formData.get('username'),
            password: formData.get('password'),
            password_confirm: formData.get('password_confirm')
        };
        
        // Проверяем валидацию формы
        if (!this.validateRegisterForm(userData)) {
            return;
        }

        try {
            this.messageManager.showLoading('Выполняется регистрация...');
            const response = await this.authClient.register(userData);
            
            this.accessToken = response.access_token;

            // Используем ApiManager для установки токена всем клиентам
            this.apiManager.setAuthToken(this.accessToken);
            
            this.hideRegisterModal();
            this.messageManager.showSuccess('Регистрация выполнена успешно!');
            
            await this.getCurrentUserInfo();
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
            this.messageManager.showLoading('Подключение Telegram...');
            const response = await this.authClient.updateTelegramUsername({telegram_username: telegramUsername});
            
            // Получаем новый access_token с обновленными данными
            this.accessToken = response.access_token;
            
            // Обновляем токены во всех клиентах
            this.apiManager.setAuthToken(this.accessToken);
            
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
        // localStorage.setItem('accessToken', this.accessToken); // Удалено
        
        // Используем ApiManager для установки токена всем клиентам
        this.apiManager.setAuthToken(this.accessToken);
    }

    // Ручной выход пользователя (по кнопке)
    async manualLogout() {
        await this.logout();
        this.messageManager.showSuccess('Выход выполнен успешно');
    }

    // Выход
    async logout() {
        try {
            if (this.accessToken) {
                await this.authClient.logout();
            }
        } catch (error) {
            console.error('Ошибка при выходе:', error);
        } finally {
            // Очищаем данные пользователя
            this.accessToken = null;
            this.currentUser = null;
            
            // Используем ApiManager для очистки токенов всех клиентов
            this.apiManager.clearAuthToken();
            
            this.showAuthButtons();
            // Не показываем сообщение об успешном выходе при автоматическом logout
        }
    }

    // Валидация формы регистрации
    validateRegisterForm(userData) {
        let isValid = true;
        
        // Очищаем предыдущие ошибки
        this.clearRegisterErrors();
        
        // Валидация username
        const username = userData.username;
        if (!username || username.length < 3) {
            this.showRegisterError('username-error', 'Минимум 3 символа');
            this.highlightField('register-username');
            isValid = false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            this.showRegisterError('username-error', 'Только буквы, цифры и подчеркивания');
            this.highlightField('register-username');
            isValid = false;
        }
        
        // Валидация пароля
        const password = userData.password;
        if (!password || password.length < 6) {
            this.showRegisterError('password-error', 'Минимум 6 символов');
            this.highlightField('register-password');
            isValid = false;
        }
        
        // Валидация подтверждения пароля
        const passwordConfirm = userData.password_confirm;
        if (password !== passwordConfirm) {
            this.showRegisterError('password-confirm-error', 'Пароли не совпадают');
            this.highlightField('register-password-confirm');
            isValid = false;
        }
        
        return isValid;
    }
    
    // Показать ошибку валидации
    showRegisterError(errorId, message) {
        const errorElement = document.getElementById(errorId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
    }
    
    // Подсветить поле с ошибкой
    highlightField(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.add('error');
        }
    }
    
    // Очистить ошибки валидации
    clearRegisterErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.classList.remove('show');
            element.textContent = '';
        });
        
        const fields = document.querySelectorAll('#register-form input');
        fields.forEach(field => {
            field.classList.remove('error');
        });
    }
}

// Глобальные функции для кнопок в карточках
function deleteVacancy(vacancyId) {
    // Удаляем confirm, удаление теперь только через кастомную модалку
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

// Модалка подтверждения удаления вакансии
function showDeleteVacancyModal(vacancyId) {
    modalManager.createConfirmModal({
        title: 'Удалить вакансию?',
        message: 'Вы уверены, что хотите удалить вакансию?',
        confirmText: 'Удалить',
        cancelText: 'Отмена',
        onConfirm: () => deleteVacancy(vacancyId)
    });
}

// Инициализация приложения
const app = new App();
window.app = app; 