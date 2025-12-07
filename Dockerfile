# Используем официальный Python
FROM python:3.12-slim

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Рабочая директория
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт Django
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]