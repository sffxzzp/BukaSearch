#!/bin/sh
wget https://github.com/sffxzzp/BukaSearch/raw/master/buka.db

rm -rf /tmp/cron.`whoami`
echo "0 0 3 ? * SUN /var/www/html/cron.sh" >> /tmp/cron.`whoami`
crontab -u `whoami` /tmp/cron.`whoami`
crond

php-fpm & nginx '-g daemon off;'