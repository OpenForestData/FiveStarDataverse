#!/bin/bash
/app/scripts/wait_for.sh ofdAgregatorRedisFiveStar:6379 -t 15 -- echo "Redis (ofdAgregatorRedisFiveStar) is up!"

printf "%s\n" "Collectstatic"
python /app/manage.py collectstatic --noinput

printf "%s\n" "Uruchamianie skryptu rate five star"
chmod +x /app/rate_five_star.py
nohup /app/rate_five_star.py &

printf "%s\n" "Uruchamianie aplikacji"
python /app/manage.py runserver 0.0.0.0:8000
