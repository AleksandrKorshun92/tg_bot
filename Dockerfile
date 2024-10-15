# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /code
# Копируем файлы requirements.txt и устанавливаем зависимости
COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# Копируем весь проект в контейнер
COPY . .
# Команда для запуска бота
CMD ["python", "main.py"]

