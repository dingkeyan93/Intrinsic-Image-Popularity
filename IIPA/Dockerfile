# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:alpine

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME ./
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec python -m gunicorn IIPA.asgi:application -w 4 -k uvicorn.workers.UvicornWorker 