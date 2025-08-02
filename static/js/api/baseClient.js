// Базовый API клиент для HTTP запросов
class BaseClient {
    constructor(clientURL = '') {
        const baseURL = '/api/public';
        this.baseURL = baseURL + clientURL;
        this.accessToken = null;
        this.isRefreshing = false;
        this.refreshPromise = null;
    }

    // Устанавливает токен авторизации
    setAuthToken(token) {
        this.accessToken = token;
    }

    // Очищает токен авторизации
    clearAuthToken() {
        this.accessToken = null;
    }

    // Валидация параметров запроса
    _validateParams(url, options = {}) {
        if (!url || typeof url !== 'string') {
            throw new Error(ERROR_MESSAGES.INVALID_URL);
        }
        
        if (options && typeof options !== 'object') {
            throw new Error(ERROR_MESSAGES.INVALID_OPTIONS);
        }
    }

    // Обработка ошибок API
    _handleApiError(response, errorData) {
        const status = response.status;
        const detail = errorData?.detail || `HTTP ${status}: ${response.statusText}`;
        
        switch (status) {
            case HTTP_STATUS.BAD_REQUEST:
                throw new Error(`Некорректный запрос: ${detail}`);
            case HTTP_STATUS.UNAUTHORIZED:
                throw new Error(ERROR_MESSAGES.AUTHENTICATION_REQUIRED);
            case HTTP_STATUS.FORBIDDEN:
                throw new Error(ERROR_MESSAGES.ACCESS_DENIED);
            case HTTP_STATUS.NOT_FOUND:
                throw new Error(ERROR_MESSAGES.RESOURCE_NOT_FOUND);
            case HTTP_STATUS.UNPROCESSABLE_ENTITY:
                throw new Error(`${ERROR_MESSAGES.VALIDATION_ERROR}: ${detail}`);
            case HTTP_STATUS.INTERNAL_SERVER_ERROR:
                throw new Error(ERROR_MESSAGES.SERVER_ERROR);
            default:
                throw new Error(detail);
        }
    }

    async request(url, options = {}, skipAuth = false) {
        // Валидация параметров
        this._validateParams(url, options);
        
        const fullUrl = this.baseURL + url;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // TODO: <-- проверить влияние на ошибку
        };

        // Добавляем токен авторизации, если он есть и не пропускаем auth
        if (this.accessToken && !skipAuth) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const requestOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(fullUrl, requestOptions);
            
            // Обработка 401 ошибки - попытка обновления токена (только если не пропускаем auth)
            if (response.status === 401 && this.accessToken && !skipAuth) {
                try {
                    // Используем AuthClient для обновления токена
                    if (window.app && window.app.authClient) {
                        const data = await window.app.authClient.refreshToken();
                        this.accessToken = data.access_token;
                        
                        // Обновляем токен во всех клиентах
                        if (window.app) {
                            window.app.updateTokens(data.access_token);
                        }
                        
                        // Повторяем запрос с новым токеном
                        if (this.accessToken) {
                            requestOptions.headers['Authorization'] = `Bearer ${this.accessToken}`;
                            const retryResponse = await fetch(fullUrl, requestOptions);
                            
                            if (retryResponse.ok) {
                                const contentType = retryResponse.headers.get('content-type');
                                if (contentType && contentType.includes('application/json')) {
                                    return await retryResponse.json();
                                }
                                return await retryResponse.text();
                            } else {
                                // Если повторный запрос тоже не удался
                                if (retryResponse.status === 401 || retryResponse.status === 403) {
                                    if (window.app) {
                                        await window.app.logout();
                                    }
                                    throw new Error('Требуется авторизация');
                                }
                                
                                const errorData = await retryResponse.json().catch(() => ({}));
                                this._handleApiError(retryResponse, errorData);
                            }
                        }
                    } else {
                        throw new Error('AuthClient недоступен');
                    }
                } catch (refreshError) {
                    // Если обновление не удалось - выходим из системы
                    if (window.app) {
                        await window.app.logout();
                    }
                    throw new Error('Требуется авторизация');
                }
            }

            // Обработка ошибок аутентификации (только для первого запроса, не retry)
            if (response.status === 401 || response.status === 403) {
                if (window.app) {
                    await window.app.logout();
                }
                throw new Error('Требуется авторизация');
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                this._handleApiError(response, errorData);
            }

            // Проверяем, есть ли контент для парсинга
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Выполняет GET запрос
    async get(url, options = {}) {
        return this.request(url, {
            method: 'GET',
            ...options,
        });
    }

    // Выполняет POST запрос
    async post(url, data = null, options = {}) {
        return this.request(url, {
            method: 'POST',
            body: data ? JSON.stringify(data) : null,
            ...options,
        });
    }

    // Выполняет PUT запрос
    async put(url, data = null, options = {}) {
        return this.request(url, {
            method: 'PUT',
            body: data ? JSON.stringify(data) : null,
            ...options,
        });
    }

    // Выполняет DELETE запрос
    async delete(url, options = {}) {
        return this.request(url, {
            method: 'DELETE',
            ...options,
        });
    }
} 