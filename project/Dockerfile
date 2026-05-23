# Создаём образ на базе легковесного Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменную окружения для импорта модулей
ENV PYTHONPATH=/app

# Открываем порт для Streamlit (по умолчанию 8501)
EXPOSE 8501

# Запускаем Streamlit-приложение
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.address", "0.0.0.0"]