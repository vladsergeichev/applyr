class FavoriteClient extends BaseClient {
    constructor() {
        super('/favorite');
    }

    async updateNotes(vacancyId, favoriteData) {
        return this.put(`/${vacancyId}`, favoriteData);
    }
} 