FROM python:3.10 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    pip install psycopg2-binary

COPY src/ .
COPY docker/backend/wsgi-entrypoint.sh /

RUN chmod +x /wsgi-entrypoint.sh
