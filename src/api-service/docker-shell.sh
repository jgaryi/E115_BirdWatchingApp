#!/bin/bash

set -e

# Define some environment variables
export IMAGE_NAME="bird-app-api-service"
export BASE_DIR=$(pwd)
export SECRETS_FILE="/mnt/c/Users/jgary/Tutorial23-25_Backend_FastAPI/secrets/ml-workflow.json"
export PERSISTENT_DIR="/mnt/c/Users/jgary/Tutorial23-25_Backend_FastAPI/persistent-folder"
export GCP_PROJECT="class2-449500" 
export GCS_BUCKET_NAME="bird-app-models"
export CHROMADB_HOST="bird-app-vector-db"
export CHROMADB_PORT=8000
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/ml-workflow.json"

# Check if the secrets file exists
echo "Checking for secret at: $SECRETS_FILE"
if [ ! -f "$SECRETS_FILE" ]; then
  echo "Missing secrets file: $SECRETS_FILE"
  exit 1
fi

# Create the network if we don't have it yet
docker network inspect bird-app-network >/dev/null 2>&1 || docker network create bird-app-network

# Build the image
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
  -v "$BASE_DIR":/app \
  -v "${SECRETS_FILE}:/secrets/ml-workflow.json" \
  -v "$PERSISTENT_DIR":/persistent \
  -p 9000:9000 \
  -e DEV=1 \
  -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
  -e GCP_PROJECT=$GCP_PROJECT \
  -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
  -e CHROMADB_HOST=$CHROMADB_HOST \
  -e CHROMADB_PORT=$CHROMADB_PORT \
  --network bird-app-network \
  $IMAGE_NAME