### Charity Fund API

### Описание
API для приложения по сбору средств на благотворительность. Реализованно на FastAPI.

### Развертывание

1. Перейти в директорию проекта, развернуть и активировать venv
2. Установить все зависимости ```pip install -r requirements.txt```
3. Добавить файл .env с полем DATABASE_URL, стандартное значение можно взять в файле app/core/config
4. С помощью сервера uvicorn запускаем сервер командой ```uvicorn app.main:app --reload```

Сервере станет доступен на локальном хосте по адресу http://localhost:8000

Можно найти интеррактивную документацию API Swagger по адресу http://localhost:8000/docs

### Системные требования
Python >= 3.9 + requirements

### Стек
SQLAlchemy, Alembic, FastAPI, uvicorn
