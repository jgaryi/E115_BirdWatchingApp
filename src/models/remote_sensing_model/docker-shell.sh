#!/bin/bash

# Set variables
IMAGE_NAME="my-python-image"
CONTAINER_NAME="my-python-container"
DOCKERFILE="Dockerfile"
PYTHON_SCRIPT="birdlocations.py"

# Ensure the Python script exists (this check is removed as we no longer run the script)
if [[ ! -f "$DOCKERFILE" ]]; then
    echo "Error: Dockerfile not found in the current directory!"
    exit 1
fi

# Build the image (if not already built)
echo "Building Docker image '$IMAGE_NAME'..."
docker build -t $IMAGE_NAME -f $DOCKERFILE .

# Exit if the build fails
if [[ $? -ne 0 ]]; then
    echo "Docker build failed. Exiting..."
    exit 1
fi

# Get the absolute path of the current script's directory (adapted for Windows)
WORKDIR=$(dirname $(realpath $0))

# Convert Windows path to Docker-compatible path (e.g. C:\Users\Username -> /c/Users/Username)
WORKDIR=$(echo $WORKDIR | sed 's/^/\/c\//;s/\\/\//g')

# Run the container but do not execute the Python script
echo "Starting container '$CONTAINER_NAME' with image '$IMAGE_NAME'..."

# Run Docker command with the absolute path for Windows, without running the Python script
docker run --rm --name $IMAGE_NAME -ti -v "$(dirname $(realpath $0))/:/app" $IMAGE_NAME
