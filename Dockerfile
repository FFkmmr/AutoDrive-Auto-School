FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/autoschool \
    DJANGO_SETTINGS_MODULE=autoschool.autoschool.settings

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python -m django collectstatic --noinput && gunicorn autoschool.autoschool.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2"]
