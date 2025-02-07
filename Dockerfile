# Используем легковесный образ Python
FROM python:3.13-slim

# Создаем директорию для приложения
RUN mkdir /booking
WORKDIR /booking

# Устанавливаем переменные окружения
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PATH="/booking/.local/bin:$PATH"

# Устанавливаем системные зависимости и очищается кэш apt после установки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN python --version && pip --version
RUN pip install --upgrade pip && pip install poetry==2.0.1

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем весь проект
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Делаем файлы в каталоге docker исполняемыми, для возможности запуска через bash
RUN chmod +x /booking/docker/*.sh

# Указываем точку входа
ENTRYPOINT ["poetry", "run"]

# Запуск Gunicorn через Poetry
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]