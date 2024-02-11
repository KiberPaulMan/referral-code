# Запуск проекта
#### Создание и запуск виртуального окружения в директории:
1. python -m venv venv
2. \venv\Scripts\activate
   
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
	<http://127.0.0.1:8000/register/>
	
#### Регистрация пользователя по реферальному коду:
	Пример реферального кода: <http://127.0.0.1:8000/reg/A9u2j3Esq4/>
	
#### Регистрация пользователя по email реферера:
	<http://127.0.0.1:8000/email-register/>
	
#### Документация по API:
	<http://127.0.0.1:8000/swagger/>
	<http://127.0.0.1:8000/redoc/>
