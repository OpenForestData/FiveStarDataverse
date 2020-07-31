#!/bin/bash
/app/scripts/wait_for.sh ofdAgregatorRedis:6379 -t 15 -- echo "Redis (ofdAgregatorRedis) is up!"

python /app/manage.py collectstatic --noinput

python /app/manage.py runserver 0.0.0.0:8000
