FROM python:3.7.0-slim

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY healthcheck.py ./
COPY run_dev.py ./
COPY config.py ./
