FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SETTINGS_MODULE=autoschool.autoschool.settings \
    SECRET_KEY=collectstatic-build-key \
    DEBUG=0 \
    python autoschool/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "gunicorn autoschool.autoschool.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2"]
