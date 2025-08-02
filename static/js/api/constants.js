// Константы для API клиентов

// HTTP статус коды
const HTTP_STATUS = {
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    UNPROCESSABLE_ENTITY: 422,
    INTERNAL_SERVER_ERROR: 500
};


// Сообщения об ошибках
const ERROR_MESSAGES = {
    INVALID_URL: 'URL должен быть строкой',
    INVALID_OPTIONS: 'Options должен быть объектом',
    INVALID_USER_DATA: 'Данные пользователя должны быть объектом',
    INVALID_VACANCY_DATA: 'Данные вакансии должны быть объектом',
    INVALID_STAGE_DATA: 'Данные этапа должны быть объектом',
    INVALID_ID: 'ID должен быть строкой или числом',
    AUTHENTICATION_REQUIRED: 'Требуется авторизация',
    ACCESS_DENIED: 'Доступ запрещен',
    RESOURCE_NOT_FOUND: 'Ресурс не найден',
    VALIDATION_ERROR: 'Ошибка валидации',
    SERVER_ERROR: 'Внутренняя ошибка сервера'
};
