# Запуск проекта
### Создание виртуального окружения в директории:
  - python -m venv venv
### Запуск виртуального окружения:
   - .\venv\Scripts\activate
### Установка зависимостей:
  - pip install -r .\requirements.txt
### Применение миграций:
  - python manage.py migrate
### Создание таблицы кеша:
 - python manage.py createcachetable
### Создание суперпользователя:
 - python manage.py createsuperuser
### Запуск локального сервера:
 - python manage.py runserver
