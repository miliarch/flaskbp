# Build app container
# Note: build context in {app-root}/docker-compose.yml must point to . for build to succeed
FROM python:3.7.0-slim

# Set workdir
WORKDIR /opt/app

# Copy and install requirements
COPY containers/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY flaskbp ./flaskbp/

# Copy configuration and supporting scripts
COPY run_app.py config.py containers/app/healthcheck.py ./
