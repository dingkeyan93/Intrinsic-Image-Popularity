# Use the official lightweight Python image.
# https://hub.docker.com/_/python
# syntax=docker/dockerfile:experimental
FROM python:3.10.13 as builder

# Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True
ARG AWS_ACCESS_KEY
ARG AWS_SECRET_KEY
ENV PIPENV_VENV_IN_PROJECT=1
ENV AWS_CONFIG_FILE /.aws/config

RUN mkdir -pv -m 700 /iipa-workspace
ENV APP_HOME /iipa-workspace
WORKDIR $APP_HOME 


ADD Pipfile.lock Pipfile ${APP_HOME}/
WORKDIR $APP_HOME


# Install production dependencies.
RUN pip install pipenv
RUN pipenv install


# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# FROM python:3.10.13 as runtime

# RUN mkdir -p /workspace 
# ENV APP_HOME /workspace
# WORKDIR $APP_HOME/

COPY ./ $APP_HOME/


# RUN mkdir -pv -m 700 .venv
# RUN mkdir -pv -m 700 django-polls

# COPY --from=builder /workspace/.venv/ .venv/
# COPY --from=builder /workspace/django-polls/ django-polls/ 


WORKDIR $APP_HOME/IIPA
# # RUN python manage.py flush --noinput
# # RUN python manage.py migrate
ENV GCP_DEV True

 
# RUN pip install --upgrade pip
# RUN pipenv requirements > reqsA.txt
# RUN grep -rl 'django-polls' requirements.txt | xargs sed 's/django-polls/\/django-polls/' > requirements.txt
# RUN pip install -r requirements.txt

RUN ../.venv/bin/python manage.py makemigrations
RUN ../.venv/bin/python manage.py migrate
# ENV DJANGO_SUPERUSER_EMAIL jazwickler@gmail.com 
# ENV DJANGO_SUPERUSER_USERNAME moose

# RUN ../.venv/bin/python manage.py createsuperuser --noinput


CMD ["../.venv/bin/python", "-m", "gunicorn", "IIPA.asgi:application", "--bind" ,":8000" ,"--log-level", "debug", "--workers", "4","--timeout", "0" ,"-k", "uvicorn.workers.UvicornWorker" ,"-c", "gunicorn.conf.py"]

EXPOSE 8000
