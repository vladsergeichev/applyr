-- Скрипт для полной очистки базы данных
-- Удаляет все таблицы, индексы, последовательности и функции

-- Отключаем проверку внешних ключей
SET session_replication_role = replica;

-- Удаляем все таблицы
DROP TABLE IF EXISTS apply_states CASCADE;
DROP TABLE IF EXISTS applies CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS states CASCADE;

-- Удаляем все последовательности
DROP SEQUENCE IF EXISTS states_id_seq CASCADE;

-- Удаляем все функции
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Включаем обратно проверку внешних ключей
SET session_replication_role = DEFAULT; 