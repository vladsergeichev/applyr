#!/bin/bash

# Подставляем переменные окружения в конфигурацию nginx
envsubst '${DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Проверяем конфигурацию nginx
nginx -t

# Запускаем nginx
exec nginx -g "daemon off;" 