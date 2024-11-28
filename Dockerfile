# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
COPY page_analyzer ./page_analyzer
COPY database.sql ./

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Переменные окружения
ENV FLASK_APP=page_analyzer:app
ENV PORT=8000

# Открываем порт приложения
EXPOSE $PORT

# Запуск приложения
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "page_analyzer:app"]
