class FavoriteClient extends BaseClient {
    constructor() {
        super('/favorite');
    }

    async updateNotes(vacancyId, notes) {
        return this.post(`/${vacancyId}/update_notes`, {notes});
    }
} 