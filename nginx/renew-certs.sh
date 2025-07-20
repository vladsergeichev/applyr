#!/bin/bash

# Скрипт для обновления SSL сертификатов Let's Encrypt

echo "Starting SSL certificate renewal..."

# Обновляем сертификаты
docker-compose run --rm certbot renew

# Перезапускаем nginx для применения новых сертификатов
docker-compose restart nginx

echo "SSL certificate renewal completed!" 