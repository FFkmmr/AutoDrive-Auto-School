import os
import sys

# Текущий файл: /app/autoschool/manage.py
# Нужно добавить в sys.path родительскую папку (repo root: /app),
# чтобы импорт пакета autoschool.autoschool работал корректно.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))      # /app/autoschool
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)                   # /app
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoschool.autoschool.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()