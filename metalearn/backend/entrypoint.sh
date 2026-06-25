#!/bin/sh
set -e

cd /var/www

if [ ! -f vendor/autoload.php ]; then
    composer install --optimize-autoloader
fi

php artisan reverb:start --no-interaction --host=0.0.0.0 --port=8080 &

exec php artisan serve --host=0.0.0.0 --port=8000
