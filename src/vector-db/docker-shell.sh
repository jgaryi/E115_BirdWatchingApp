#!/bin/bash
set -e

# Use absolute path directly
export SECRETS_FILE="/mnt/c/Users/jgary/Tutorial23-25_Backend_FastAPI/secrets/llm-service-account.json"
export BASE_DIR=$(pwd)
export GCP_PROJECT="class2-449500"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"
export IMAGE_NAME="bird-app-vector-db-cli"

# Check if secret exists
echo "Checking for secret at: $SECRETS_FILE"
if [ ! -f "$SECRETS_FILE" ]; then
  echo "Missing secrets file: $SECRETS_FILE"
  exit 1
fi

# Create the network if we don't have it yet
docker network inspect bird-app-network >/dev/null 2>&1 || docker network create bird-app-network

# Build the image
docker build -t $IMAGE_NAME -f Dockerfile .

# Run container with secret mounted
docker-compose run --rm --service-ports \
  -v "$SECRETS_FILE:/secrets/llm-service-account.json" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json" \
  $IMAGE_NAME