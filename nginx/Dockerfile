FROM nginx:alpine

# Устанавливаем envsubst для подстановки переменных
RUN apk add --no-cache bash

# Создаем директорию для Let's Encrypt webroot
RUN mkdir -p /var/www/html

# Копируем конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf.template

# Создаем пустой файл для проверки
RUN echo "Let's Encrypt webroot" > /var/www/html/index.html

# Создаем скрипт запуска
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80 443

ENTRYPOINT ["/docker-entrypoint.sh"] 