// Основное приложение
class App {
    constructor() {
        // Сначала создаем window.app для доступа из других компонентов
        window.app = this;

        // Используем ApiManager для централизованного управления клиентами
        this.apiManager = new ApiManager();
        this.authClient = this.apiManager.authClient;
        this.vacancyClient = this.apiManager.vacancyClient;
        this.favoriteClient = this.apiManager.favoriteClient;
        this.stageClient = this.apiManager.stageClient;

        this.messageManager = new MessageManager();
        this.vacancyRenderer = new VacancyRenderer();
        this.vacancyDetailsRenderer = new VacancyDetailsRenderer();
        this.router = new Router();

        this.currentUser = null;
        this.accessToken = null;

        // Инициализируем приложение асинхронно
        (async () => {
            try {
                await this.initializeApp();
            } catch (error) {
                console.error('Error initializing app:', error);
            }
        })();
    }

    async initializeApp() {
        this.setupEventListeners();
        await this.checkAuthStatus();
    }

    setupEventListeners() {
        // Кнопка входа
        const loginBtn = document.getElementById('login-btn');
        loginBtn.addEventListener('click', () => this.showLoginModal());

        // Кнопка профиля и выпадающее меню
        const profileBtn = document.getElementById('profile-btn');
        const dropdownIcon = profileBtn?.querySelector('.dropdown-icon');
        const profileDropdownContainer = document.querySelector('.user-profile');

        if (profileBtn && dropdownIcon && profileDropdownContainer) {
            const dropdown = new Dropdown({
                triggerButton: profileBtn,
                items: [
                    {
                        text: 'Выход',
                        className: 'clr-red',
                        onClick: () => this.logout()
                    }
                ],
                onShow: () => dropdownIcon.classList.add('open'),
                onHide: () => dropdownIcon.classList.remove('open')
            });

            profileDropdownContainer.appendChild(dropdown.getContainer());
        }

        // Кнопка выхода больше не нужна, так как обработчик добавляется в дропдауне
    }

    async checkAuthStatus() {
        // Пытаемся получить access_token через refresh_token
        await this.tryRefreshToken();
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
            // Инициализируем роутер даже при ошибке авторизации
            this.setupRouter();
            await this.router.handleRoute();
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
            this.showVacanciesContainer();
            this.updateUserInfo();

            if (showWelcomeMessage) {
                this.messageManager.showSuccess(`Добро пожаловать, ${userInfo.alias}!`);
            }

            // Настраиваем роутер после успешной авторизации
            this.setupRouter();

            // Обрабатываем текущий URL
            await this.router.handleRoute();
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
            userInfoElement.textContent = this.currentUser.alias;
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
    setupRouter() {
        // Главная страница
        this.router.addRoute('/', async () => {
            document.getElementById('vacancy-container').classList.add('hidden');
            if (this.currentUser) {
                this.showVacanciesContainer();
                await this.loadUserVacancies();
            } else {
                this.showAuthButtons();
            }
        });

        // Детальная страница вакансии
        this.router.addRoute('/vacancy/:id', async (params) => {
            if (this.currentUser) {
                await this.vacancyDetailsRenderer.render(params.id);
                document.getElementById('vacancy-container').classList.remove('hidden');
            } else {
                this.showAuthButtons();
                this.router.navigate('/', true); // Редирект на главную если не авторизован
            }
        });
    }

    async loadUserVacancies() {
        if (!this.currentUser) {
            return;
        }

        try {
            // Обновляем ссылку на список вакансий после пересоздания DOM
            this.vacancyRenderer.updateVacanciesList();

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
        document.getElementById('vacancies-container').classList.add('hidden');
        document.getElementById('vacancy-container').classList.add('hidden');
    }

    showVacanciesContainer() {
        document.getElementById('login-btn').classList.add('hidden');
        document.getElementById('user-info').classList.remove('hidden');
        document.getElementById('vacancies-container').classList.remove('hidden');
    }

    // Модальные окна
    showLoginModal() {
        const formContent = `
            <div class="form-group">
                <label for="login-username">Логин:</label>
                <input type="text" id="login-username" name="username" required>
            </div>
            <div class="form-group">
                <label for="login-password">Пароль:</label>
                <input type="password" id="login-password" name="password" required>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Войти</button>
                <button type="button" class="btn btn-secondary" id="switch-to-register">Регистрация</button>
            </div>
        `;

        const modalId = modalManager.createFormModal({
            title: 'Вход в систему',
            formContent,
            onSubmit: (e, modalId) => {
                this.handleLogin(e);
                modalManager.closeModal(modalId);
            },
            onCancel: () => {
                modalManager.closeModal(modalId);
            }
        });

        // Добавляем обработчик для кнопки переключения на регистрацию
        document.getElementById('switch-to-register').addEventListener('click', () => {
            modalManager.closeModal(modalId);
            this.showRegisterModal();
        });
    }

    showRegisterModal() {
        console.log('Opening register modal');
        const formContent = `
            <div class="form-group">
                <label for="register-username">Логин:</label>
                <input type="text" id="register-username" name="username" required>
                <div class="error-message" id="username-error"></div>
            </div>
            <div class="form-group">
                <label for="register-first-name">Имя:</label>
                <input type="text" id="register-first-name" name="first_name" required>
                <div class="error-message" id="first-name-error"></div>
            </div>
            <div class="form-group">
                <label for="register-second-name">Фамилия:</label>
                <input type="text" id="register-second-name" name="second_name" required>
                <div class="error-message" id="second-name-error"></div>
            </div>
            <div class="form-group">
                <label for="register-email">Email:</label>
                <input type="email" id="register-email" name="email" required>
                <div class="error-message" id="email-error"></div>
            </div>
            <div class="form-group">
                <label for="register-password">Пароль:</label>
                <input type="password" id="register-password" name="password" required>
                <div class="error-message" id="password-error"></div>
            </div>
            <div class="form-group">
                <label for="register-password-confirm">Подтвердите пароль:</label>
                <input type="password" id="register-password-confirm" name="password_confirm" required>
                <div class="error-message" id="password-confirm-error"></div>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
                <button type="button" class="btn btn-secondary" id="switch-to-login">Войти</button>
            </div>
        `;

        const modalId = modalManager.createFormModal({
            title: 'Регистрация',
            formContent,
            onSubmit: (e) => {
                this.handleRegister(e);
            },
            onCancel: () => {
                modalManager.closeModal(modalId);
            }
        });

        // Добавляем обработчик для кнопки переключения на вход
        document.getElementById('switch-to-login').addEventListener('click', () => {
            modalManager.closeModal(modalId);
            this.showLoginModal();
        });

        // Добавляем обработчики для очистки ошибок при вводе
        const registerInputs = document.querySelectorAll('#form-' + modalId + ' input');
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

    showTelegramModal() {
        const formContent = `
            <div class="form-group">
                <label for="telegram-username">Telegram Username:</label>
                <input type="text" id="telegram-username" name="telegram_username" placeholder="@username" required>
                <small>Введите ваш Telegram username без символа @</small>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Подключить</button>
                <button type="button" class="btn btn-secondary" id="cancel-telegram">Отмена</button>
            </div>
        `;

        const modalId = modalManager.createFormModal({
            title: 'Подключение Telegram',
            formContent,
            onSubmit: (e, modalId) => {
                this.handleTelegramConnect(e);
                modalManager.closeModal(modalId);
            },
            onCancel: () => {
                modalManager.closeModal(modalId);
            }
        });

        // Добавляем обработчик для кнопки отмены
        document.getElementById('cancel-telegram').addEventListener('click', () => {
            modalManager.closeModal(modalId);
        });
    }

    hideAllModals() {
        modalManager.closeAllModals();
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

            // Используем ApiManager для установки токена всем клиентам
            this.apiManager.setAuthToken(this.accessToken);

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
            first_name: formData.get('first_name'),
            second_name: formData.get('second_name'),
            email: formData.get('email'),
            password: formData.get('password'),
            password_confirm: formData.get('password_confirm')
        };

        // Проверяем валидацию формы
        if (!this.validateRegisterForm(userData)) {
            return;
        }

        try {
            const response = await this.authClient.register(userData);

            this.accessToken = response.access_token;

            // Используем ApiManager для установки токена всем клиентам
            this.apiManager.setAuthToken(this.accessToken);

            modalManager.closeAllModals();

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

            modalManager.closeAllModals();

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

        console.log('Starting validation for:', userData);
        // Очищаем предыдущие ошибки
        this.clearRegisterErrors();

        // Валидация username
        const username = userData.username;
        console.log('Validating username:', username);
        if (!username || username.length < 3) {
            console.log('Username validation failed: too short');
            this.showRegisterError('username-error', 'Минимум 3 символа');
            this.highlightField('register-username');
            isValid = false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            console.log('Username validation failed: invalid characters');
            this.showRegisterError('username-error', 'Только буквы, цифры и подчеркивания');
            this.highlightField('register-username');
            isValid = false;
        }

        // Валидация имени
        const firstName = userData.first_name;
        if (!firstName || firstName.length < 2) {
            this.showRegisterError('first-name-error', 'Минимум 2 символа');
            this.highlightField('register-first-name');
            isValid = false;
        }

        // Валидация фамилии
        const secondName = userData.second_name;
        if (!secondName || secondName.length < 2) {
            this.showRegisterError('second-name-error', 'Минимум 2 символа');
            this.highlightField('register-second-name');
            isValid = false;
        }

        // Валидация email
        const email = userData.email;
        if (!email || !/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(email)) {
            this.showRegisterError('email-error', 'Некорректный формат email');
            this.highlightField('register-email');
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