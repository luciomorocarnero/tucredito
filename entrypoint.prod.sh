#!/bin/bash

set -e  # hace que falle el script si cualquier comando devuelve error

until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USERNAME
do
    echo "Esperando a que la base de datos esté lista..."
    sleep 2
done

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Intentando crear superusuario..."
python manage.py createsuperuser --noinput || echo "El superusuario ya existe o no se pudo crear."

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Lanzar Daphne
echo "Iniciando Daphne..."
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
