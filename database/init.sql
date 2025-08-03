-- Создание таблиц для системы управления откликами

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY, -- telegram_id
    username VARCHAR(255) UNIQUE, -- telegram username
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица состояний
CREATE TABLE IF NOT EXISTS states (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица откликов
CREATE TABLE IF NOT EXISTS applies (
    id VARCHAR(64) PRIMARY KEY, -- хэш-идентификатор
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL, -- название вакансии
    link TEXT NOT NULL, -- ссылка на вакансию
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица состояний откликов
CREATE TABLE IF NOT EXISTS apply_states (
    id VARCHAR(64) PRIMARY KEY, -- хэш-идентификатор
    vacancy_id VARCHAR(64) NOT NULL REFERENCES applies(id) ON DELETE CASCADE,
    state_id INTEGER NOT NULL REFERENCES states(id) ON DELETE CASCADE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов
CREATE INDEX IF NOT EXISTS idx_applies_user_id ON applies(user_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_apply_states_vacancy_id ON apply_states(vacancy_id);
CREATE INDEX IF NOT EXISTS idx_apply_states_state_id ON apply_states(state_id);

-- Вставка базовых состояний
INSERT INTO states (name) VALUES 
    ('Создан'),
    ('Отправлено'),
    ('Ответ получен'),
    ('Приглашение на собеседование'),
    ('Собеседование пройдено'),
    ('Отклонено'),
    ('Принят')
ON CONFLICT (name) DO NOTHING;

-- Функция для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггеры для автоматического обновления updated_at
CREATE TRIGGER update_applies_updated_at 
    BEFORE UPDATE ON applies 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_apply_states_updated_at 
    BEFORE UPDATE ON apply_states 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 