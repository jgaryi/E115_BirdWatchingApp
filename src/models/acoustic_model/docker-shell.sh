#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="bird_acoustic_model"
# export BASE_DIR="C:/Users/yongl/E115/Project/BirdNET-Analyzer"

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container, for windows system, use absolute folder path instead of "pwd"
docker run --rm --name $IMAGE_NAME -ti -v "/your/folder/path":/app $IMAGE_NAME
