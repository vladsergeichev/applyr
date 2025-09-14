class Router {
    constructor() {
        this.routes = new Map();
        this.currentRoute = null;

        // Обработка навигации браузера
        window.addEventListener('popstate', (e) => this.handlePopState(e));
    }

    // Добавление маршрута
    addRoute(path, handler) {
        this.routes.set(path, handler);
    }

    // Получение параметров из URL
    getUrlParams(pattern, url) {
        const paramNames = pattern.match(/:\w+/g) || [];
        const paramValues = url.match(new RegExp(pattern.replace(/:\w+/g, '([^/]+)')));

        if (!paramValues) return null;

        const params = {};
        paramNames.forEach((name, index) => {
            params[name.slice(1)] = paramValues[index + 1];
        });

        return params;
    }

    // Обработка изменения URL
    async handleRoute(url = window.location.pathname) {
        for (const [pattern, handler] of this.routes) {
            const regexPattern = pattern.replace(/:\w+/g, '([^/]+)');
            const regex = new RegExp(`^${regexPattern}$`);

            if (regex.test(url)) {
                const params = this.getUrlParams(pattern, url);
                this.currentRoute = {pattern, params};
                await handler(params);
                return true;
            }
        }
        return false;
    }

    // Навигация к новому URL
    async navigate(url, replaceState = false) {
        const method = replaceState ? 'replaceState' : 'pushState';
        window[`history`][method]({}, '', url);
        return this.handleRoute(url);
    }

    // Обработка навигации браузера
    async handlePopState() {
        await this.handleRoute();
    }
}
