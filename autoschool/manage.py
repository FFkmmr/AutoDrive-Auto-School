import os
import sys

# Добавляем корневую папку проекта /app/autoschool в sys.path,
# чтобы импорты вроде "main" и пакет autoschool.autoschool работали при сборке.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /app/autoschool
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoschool.autoschool.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()