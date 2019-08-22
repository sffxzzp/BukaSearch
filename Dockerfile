FROM php:fpm-alpine
COPY . .
RUN apk add --no-cache nginx tzdata wget cron && \
    mkdir -p /run/nginx && \
    mv default.conf /etc/nginx/conf.d && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    chmod +x entrypoint.sh && \
    chmod +x cron.sh && \
    wget https://raw.githubusercontent.com/catfan/Medoo/master/src/Medoo.php

EXPOSE 80
ENTRYPOINT [ "/var/www/html/entrypoint.sh" ]
