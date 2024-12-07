FROM python:3.9-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3306
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app