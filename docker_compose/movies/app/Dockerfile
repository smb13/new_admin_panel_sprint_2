FROM python:3.10

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV DB_NAME movies_database
ENV DB_USER app
ENV DB_PASSWORD 123qwe
ENV SECRET_KEY 'django-insecure-y4irzg!_ni$d6auqwi-n9u_td(w+rj!51h&@#s*gl71!llw8@d'
ENV DEBUG True
ENV ROOT_PATH /opt
ENV ALLOWED_HOSTS 127.0.0.1
ENV DB_HOST postgres
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

# Скопируйте в контейнер файлы, которые редко меняются
COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

# Установите зависимости
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . .

RUN ./run_uwsgi.sh

RUN  groupadd -r web && useradd -d /opt/app -r -g web web \
     && chown web:web -R /opt/app

USER web

# Укажите порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000

# Укажите, как запускать ваш сервис
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]