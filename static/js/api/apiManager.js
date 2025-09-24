// Централизованный менеджер API клиентов
class ApiManager {
    constructor() {
        this.authClient = new AuthClient();
        this.vacancyClient = new VacancyClient();
        this.favoriteClient = new FavoriteClient();

        this.clients = [
            this.authClient,
            this.vacancyClient,
            this.favoriteClient
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
}