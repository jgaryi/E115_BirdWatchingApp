#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Set vairables
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/
export GCP_PROJECT="gen-lang-client-0083231133" # CHANGE TO YOUR PROJECT ID
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/acoustic_monitoring_sa.json"
export IMAGE_NAME="data-scraping-cli"
export BUCKET_NAME = "acoustic_monitoring_project"
#change line 10 and line 11


# Create the network if we don't have it yet
# docker network inspect llm-rag-network >/dev/null 2>&1 || docker network create llm-rag-network

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run All Containers
docker run --rm -it \
    -v "$BASE_DIR":/app \
    -v "$SECRETS_DIR":/secrets \
    -v "$PERSISTENT_DIR":/persistent \
    -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
    -e GCP_PROJECT=$GCP_PROJECT \
    $IMAGE_NAME

