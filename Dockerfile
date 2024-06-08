# Используем базовый образ для Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

# Устанавливаем зависимости для Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Копируем проект
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запуск сервера Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
