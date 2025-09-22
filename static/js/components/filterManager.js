class FilterManager {
    constructor() {
        this.filterToggleBtn = document.getElementById('filter-toggle-btn');
        this.contentFilters = document.getElementById('content-filters');
        this.filterCloseBtn = document.querySelector('.filter-close-btn');
        
        this.initialize();
    }

    initialize() {
        if (!this.filterToggleBtn || !this.contentFilters || !this.filterCloseBtn) {
            return;
        }

        this.filterToggleBtn.addEventListener('click', () => this.toggleFilters());
        this.filterCloseBtn.addEventListener('click', () => this.closeFilters());
    }

    toggleFilters() {
        this.contentFilters.classList.toggle('show');
    }

    closeFilters() {
        this.contentFilters.classList.remove('show');
    }
}

// Инициализация менеджера фильтров
window.addEventListener('DOMContentLoaded', () => {
    window.app = window.app || {};
    window.app.filterManager = new FilterManager();
});
