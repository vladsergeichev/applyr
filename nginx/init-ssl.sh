#!/bin/bash

# Скрипт для первоначального получения SSL сертификатов

echo "Starting initial SSL certificate generation..."

# Проверяем наличие переменных окружения
if [ -z "$DOMAIN" ]; then
    echo "Error: DOMAIN environment variable is not set"
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo "Error: EMAIL environment variable is not set"
    exit 1
fi

echo "Domain: $DOMAIN"
echo "Email: $EMAIL"

# Запускаем nginx для обработки Let's Encrypt challenge
echo "Starting nginx..."
docker-compose up -d nginx

# Ждем запуска nginx
echo "Waiting for nginx to start..."
sleep 10

# Получаем сертификаты
echo "Obtaining SSL certificates..."
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/html \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Проверяем результат
if [ $? -eq 0 ]; then
    echo "SSL certificates obtained successfully!"
    echo "Restarting nginx to apply certificates..."
    docker-compose restart nginx
    echo "SSL setup completed!"
else
    echo "Error: Failed to obtain SSL certificates"
    exit 1
fi 