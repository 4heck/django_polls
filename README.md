# django_polls
![Docker Build Status](https://img.shields.io/badge/code%20style-black-000000.svg)

## Как запускать

1. Установка всех зависимостей
   
       $ poetry install

2. Применение virtualenv 

       $ poetry shell
       
3. Запуск зависимостей (postgres)

       $ docker-compose up -d
       
4. Запуск самого веб-сервера

       $ python3 manage.py runserver 0.0.0.0:8000
