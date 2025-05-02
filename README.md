# FeedHound

Асинхронный веб-сервис на FastAPI с PostgreSQL, SQLAlchemy 2.0 и Alembic.

## Установка

1. Клонируйте репозиторий:
  
   git clone git@github.com:NumiViX/FeedHound.git
   cd FeedHound

2. Установите зависимости:

poetry install


3. Создайте файл .env на основе .env.example:

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/feedhound



Миграции

1. Создание миграции:

alembic revision --autogenerate -m "create something"


2. Применение миграций:

alembic upgrade head



Запуск проекта

uvicorn app.main:app --reload

Эндпоинты

GET /sources — получить список источников

POST /sources — добавить новый источник


Стек

FastAPI

SQLAlchemy 2.0 (async)

Alembic

PostgreSQL


---

### **`.gitignore`**
gitignore
# Python
pycache/
*.py[cod]
*.egg
*.egg-info/
dist/
build/

# Env
.env
.env.*

# Virtualenv
venv/
.venv/
poetry.lock

# Alembic
alembic/versions/

# IDEs
.vscode/
.idea/
