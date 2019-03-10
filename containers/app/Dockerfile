# Build app container
# Note: build context in {app-root}/docker-compose.yml must point to . for build to succeed
FROM python:3.7.0-slim

# Set workdir and copy files
WORKDIR /opt/app
COPY flaskbp ./flaskbp/
COPY run_app.py ./
COPY config.py ./
COPY containers/app/healthcheck.py ./

COPY containers/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
