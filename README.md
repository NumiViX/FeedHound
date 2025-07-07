# FeedHound

**FeedHound** — это асинхронное веб-приложение для автоматического парсинга новостей из RSS-источников (например, Lenta, RBC) и Telegram-каналов, с автоподгрузкой новостей, API-интерфейсом, поддержкой Celery и расширенной архитектурой для будущих улучшений.

## Особенности

- Асинхронный FastAPI backend
- PostgreSQL + SQLAlchemy (Async)
- Поддержка парсинга RSS-источников
- Автоматическое обновление новостей через Celery
- Обновляемый список источников через API
- Поддержка синхронных и асинхронных парсеров
- Документация через OpenAPI (Swagger/Redoc)
- Подготовка к масштабированию: Telegram-парсинг, авторизация, логирование, кеширование

---

## Установка

```bash
git clone git@github.com:NumiViX/FeedHound.git
cd feedhound
pip install -r requirements.txt
cp .env.example .env
```

Настрой переменные окружения в `.env`.

---

## Запуск проекта

```bash
# 1. Запуск базы данных и Redis через Docker
docker-compose up -d

# 2. Применение миграций
alembic upgrade head

# 3. Запуск FastAPI сервера
uvicorn app.main:app --reload

# 4. Запуск Celery воркера
celery -A app.core.celery_app.celery worker --loglevel=info
```

---

## Структура проекта

```
app/
├── api/            # Роуты FastAPI
├── celery/         # Задачи для фоновой обработки
├── crud/           # CRUD-операции (sync и async)
├── models/         # SQLAlchemy-модели
├── parsers/        # Парсеры для новостных источников
├── schemas/        # Pydantic-схемы
├── services/       # Логика запуска парсера и бизнес-логика
├── core/           # Настройки, Celery, БД
└── main.py         # Точка входа
```

---

## Использование API

Документация доступна по адресу:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

Примеры эндпоинтов:

### Источники

- `GET /sources/` — получить список всех источников
- `POST /sources/` — создать новый источник
- `PUT /sources/{id}` — обновить источник
- `DELETE /sources/{id}` — удалить

### Новости

- `GET /news/` — получить список новостей
- `POST /news/` — создать новость вручную
- `GET /news/{id}` — получить новость по ID
- `DELETE /news/{id}` — удалить новость

### Парсинг

- `POST /sources/{source_id}/parse` — запустить парсинг источника (локально или через Celery)

---

## Настройка автоматической загрузки

Добавлен Celery для автопарсинга. Парсинг запускается как фоновая задача через Redis брокер. Планируется добавить расписание (beat) для периодического парсинга всех источников.

---

## В планах

- [ ] Авторизация и роли пользователей (JWT)
- [ ] Парсинг Telegram-каналов
- [ ] Кеширование через Redis
- [ ] Подписки на источники
- [ ] UI-админка
- [ ] Интеграционные и unit-тесты
- [ ] Логирование и мониторинг (Loguru / Flower / Prometheus)
- [ ] Докеризация (Dockerfile, docker-compose.prod)
- [ ] CI/CD пайплайн (GitHub Actions)

---

## Лицензия

MIT License

---

## Автор

[Vadim YA] — 2025