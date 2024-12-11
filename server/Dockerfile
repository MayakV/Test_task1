# Install the base requirements for the app.
# This stage is to support development
FROM python:3.12 AS base
WORKDIR home/server
COPY ../py_requirements.txt .
RUN pip install -r py_requirements.txt
COPY ./server/main.py ./bin/main.py
COPY ../utils/bq_api.py ./bin/utils/bq_api.py
COPY ../keys/service_secret.json /tmp/keys/service_secret.json

EXPOSE 5000

ENTRYPOINT python -u ./bin/main.py