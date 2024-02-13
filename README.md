# Запуск проекта
#### Создание и запуск виртуального окружения в директории:
1. python -m venv venv
2. .\venv\Scripts\activate
   
#### Установка зависимостей и применение миграций:
3. pip install -r .\requirements.txt
4. python manage.py migrate

#### Создание таблицы кеша:
5. python manage.py createcachetable
   
#### Создание суперпользователя:
6. python manage.py createsuperuser
   
#### Запуск локального сервера:
7. python manage.py runserver

# Рабочий процесс
#### Регистрация пользователя:
	<http://127.0.0.1:8000/core/api/v1/profile/register/>
	
#### Регистрация пользователя по реферальному коду (пример):
	<http://127.0.0.1:8000/core/api/v1/profile/register/GZMB7KLYE2/>
	
#### Регистрация пользователя по email реферера:
	<http://127.0.0.1:8000/core/api/v1/profile/register/>
	
#### Документация по API:
	<http://127.0.0.1:8000/swagger/>
	<http://127.0.0.1:8000/redoc/>
