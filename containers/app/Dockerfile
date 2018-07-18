FROM python:3.7.0-slim

RUN apt-get update && apt-get install netcat -y

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
