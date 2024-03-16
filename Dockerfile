FROM python:alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установим директорию для работы

WORKDIR /SouvenirPerfumeTGBot

COPY ./requirements.txt ./

# Устанавливаем зависимости и gunicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Копируем файлы и билд
ADD . /SouvenirPerfumeTGBot

RUN chmod -R 777 ./
