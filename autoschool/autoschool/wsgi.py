import os
import sys

# Добавляем в sys.path папку, где лежат приложения (чтобы импорты вроде "main" работали)
# __file__ указывает на /app/autoschool/autoschool/wsgi.py, поэтому добавляем ../ (то есть /app/autoschool)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoschool.autoschool.settings')

application = get_wsgi_application()