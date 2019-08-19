#!/bin/sh
wget https://github.com/sffxzzp/BukaSearch/raw/master/buka.db
php-fpm & nginx '-g daemon off;'
