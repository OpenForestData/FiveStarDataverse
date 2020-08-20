#!/bin/bash
/app/scripts/wait_for.sh ofdAgregatorRedisFiveStar:6379 -t 15 -- echo "Redis (ofdAgregatorRedisFiveStar) is up!"

python /app/manage.py collectstatic --noinput

python /app/five_star_data_manager.py

python /app/manage.py runserver 0.0.0.0:8000
