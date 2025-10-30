import os
import sys

# Этот файл: /app/autoschool/autoschool/wsgi.py
# Добавляем repo root (/app) в sys.path, чтобы импорты приложений и settings корректно работали.
THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))   # /app/autoschool/autoschool
PROJECT_ROOT = os.path.dirname(os.path.dirname(THIS_FILE_DIR))  # /app
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoschool.autoschool.settings')

application = get_wsgi_application()