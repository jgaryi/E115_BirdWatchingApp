FROM python:3.11-slim-buster

WORKDIR /app

# Install system dependencies
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git && \
    pip install --no-cache-dir --upgrade pip && \
    # pip install --no-cache-dir --upgrade pip && \
    pip install pipenv virtualenv

# Copy only Pipfile & Pipfile.lock first (for efficient Docker caching)
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv sync
RUN pipenv lock --clear && pipenv sync --dev  

# Copy the rest of the app
COPY . .

# Set the default shell (opens automatically when you run the container)
ENTRYPOINT ["/bin/bash"]
