# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies for pip install and clean up
RUN apt-get install debian-archive-keyring && \
    apt-get update --allow-insecure-repositories && \
    apt-get install -y build-essential libssl-dev libffi-dev python-dev-is-python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dev dependencies
RUN python -m pip install --upgrade python-dotenv==1.0.0

# Install pip requirements
COPY requirements.txt prune_azure_mgmt_libs.sh /
RUN python -m pip install -r requirements.txt
# Prune libs like in prod to keep lambda layer size down
RUN bash prune_azure_mgmt_libs.sh

WORKDIR /app
COPY . /app
# move config.env to .env if .config.env exists but continue if it doesn't
RUN test -f .config.env && mv .config.env .env || true

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src/entry.py"]
