#!/bin/bash

set -e

# Name of the image and container
export IMAGE_NAME="birdnet_app"
export CONTAINER_NAME="birdnet_app"
export BASE_DIR=$(pwd)

# Make sure the Docker network exists
docker network inspect bird-app-network >/dev/null 2>&1 || docker network create bird-app-network

# Build the image
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $CONTAINER_NAME -ti \
  -v "$BASE_DIR":/app \
  -p 9090:9090 \
  --network bird-app-network \
  $IMAGE_NAME
