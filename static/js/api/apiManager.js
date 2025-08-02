// Централизованный менеджер API клиентов
class ApiManager {
    constructor() {
        this.authClient = new AuthClient();
        this.vacancyClient = new VacancyClient();
        this.stageClient = new StageClient();
        
        this.clients = [
            this.authClient,
            this.vacancyClient,
            this.stageClient
        ];
    }

    // Устанавливает токен авторизации для всех клиентов
    setAuthToken(token) {
        this.clients.forEach(client => client.setAuthToken(token));
    }

    // Очищает токен авторизации для всех клиентов
    clearAuthToken() {
        this.clients.forEach(client => client.clearAuthToken());
    }

    // Получает клиент по имени
    getClient(clientName) {
        const clientMap = {
            'auth': this.authClient,
            'vacancy': this.vacancyClient,
            'stage': this.stageClient
        };
        return clientMap[clientName];
    }

    // Проверяет, авторизован ли пользователь
    isAuthenticated() {
        return this.authClient.accessToken !== null;
    }
} 