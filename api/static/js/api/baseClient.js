// Базовый API клиент для HTTP запросов
class BaseClient {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
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

    // Обновление токена
    async refreshToken() {
        if (this.isRefreshing) {
            return this.refreshPromise;
        }

        this.isRefreshing = true;
        this.refreshPromise = this._performRefresh();

        try {
            const result = await this.refreshPromise;
            this.isRefreshing = false;
            this.refreshPromise = null;
            return result;
        } catch (error) {
            this.isRefreshing = false;
            this.refreshPromise = null;
            throw error;
        }
    }

    // Прямой запрос без обработки 401 (для обновления токена)
    async _directRequest(url, options = {}) {
        const fullUrl = this.baseURL + url;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'omit', // По умолчанию не отправляем cookies
        };

        const requestOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        const response = await fetch(fullUrl, requestOptions);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        return await response.text();
    }

    // Выполнение обновления токена
    async _performRefresh() {
        try {
            const data = await this._directRequest('/auth/refresh', {
                method: 'POST',
                credentials: 'include',
            });

            this.accessToken = data.access_token;
            
            // Обновляем токен во всех клиентах
            if (window.app) {
                window.app.updateTokens(data.access_token);
            }

            return data;
        } catch (error) {
            // При ошибке обновления - выходим из системы
            if (window.app) {
                await window.app.logout();
            }
            throw error;
        }
    }

    async request(url, options = {}) {
        const fullUrl = this.baseURL + url;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'omit', // По умолчанию не отправляем cookies
        };

        // Добавляем токен авторизации, если он есть
        if (this.accessToken) {
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
            
            // Обработка 401 ошибки - попытка обновления токена
            if (response.status === 401 && this.accessToken) {
                try {
                    await this.refreshToken();
                    
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
                            throw new Error(errorData.detail || `HTTP ${retryResponse.status}: ${retryResponse.statusText}`);
                        }
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
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
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

    async get(url, options = {}) {
        return this.request(url, {
            method: 'GET',
            ...options,
        });
    }

    async post(url, data = null, options = {}) {
        return this.request(url, {
            method: 'POST',
            body: data ? JSON.stringify(data) : null,
            ...options,
        });
    }

    async put(url, data = null, options = {}) {
        return this.request(url, {
            method: 'PUT',
            body: data ? JSON.stringify(data) : null,
            ...options,
        });
    }

    async delete(url, options = {}) {
        return this.request(url, {
            method: 'DELETE',
            ...options,
        });
    }
} 