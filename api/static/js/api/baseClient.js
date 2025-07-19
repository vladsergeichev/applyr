// Базовый API клиент для HTTP запросов
class BaseClient {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
    }

    async request(url, options = {}) {
        const fullUrl = this.baseURL + url;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

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