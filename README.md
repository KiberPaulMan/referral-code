# Запуск проекта
  1. Создание виртуального окружения в директории:
    -  python -m venv venv
  3. Запуск виртуального окружения: .\venv\Scripts\activate
  4. Установка зависимостей:
    3.1 pip install -r .\requirements.txt
    
  5. Создание и применение миграций: 
    4.1 python manage.py makemigrations
    4.2 python manage.py migrate
    
  6. Создание таблицы кеша: python manage.py createcachetable
  5. Создание суперпользователя: python manage.py createsuperuser
  6. Запуск локального сервера: python manage.py runserver
