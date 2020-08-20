FROM python:3.6-slim-buster

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    python3-dev \
    make \
    gcc \
    git

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/wait_for.sh

CMD ["/app/scripts/entrypoint.sh"]
