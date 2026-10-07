# Task Tracker API

REST API для управления задачами, разработанный на Python с использованием FastAPI.

## Технологии

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- aiosqlite
- Uvicorn

## Возможности

- создание задачи
- получение списка задач
- получение задачи по ID
- удаление задачи
- асинхронная работа с базой данных

## Установка

Клонировать репозиторий:

```bash
git clone https://github.com/AnahitSarg/Task-tracker-using-fastAPI.git
cd Task-tracker-using-fastAPI
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать виртуальное окружение:

Windows:

```bash
venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

Запустить приложение:

```bash
uvicorn main:app --reload
```

После запуска API будет доступен по адресу:

http://127.0.0.1:8000

## Документация API

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

## Структура проекта

models/ - модели базы данных
routers/ - маршруты API
schemas/ - Pydantic-схемы
database.py - подключение к базе данных
repository.py - работа с данными
main.py - точка входа приложения
