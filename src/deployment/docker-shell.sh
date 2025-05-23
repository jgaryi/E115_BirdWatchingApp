#!/bin/bash

# exit immediately if a command exits with a non-zero status
#set -e

# Define some environment variables
export IMAGE_NAME="bird-app-deployment"
export BASE_DIR=$(realpath "$(dirname "$0")")
export SECRETS_DIR="/mnt/c/Users/jgary/Tutorial23-25_Backend_FastAPI/secrets"
export GCP_PROJECT="class2-449500"
export GCP_ZONE="us-central1-c"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/deployment.json"

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$HOME/.ssh":/home/app/.ssh \
-v "$BASE_DIR/../api-service":/api-service \
-v "$BASE_DIR/../frontend-react":/frontend-react \
-v "$BASE_DIR/../vector-db":/vector-db \
-v "$BASE_DIR/../birdnet_app":/birdnet_app \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e USE_GKE_GCLOUD_AUTH_PLUGIN=True \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
$IMAGE_NAME

