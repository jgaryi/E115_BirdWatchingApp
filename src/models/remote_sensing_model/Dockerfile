# Use the official Python base image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to avoid Python writing .pyc files to the container's filesystem
# and to ensure that it is running in a non-interactive mode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory
WORKDIR /app

# Install the necessary system dependencies for geemap
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /app/

# Install the Python dependencies from the Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application files into the container
COPY . /app/

# Set the entry point to run the script
CMD ["pipenv", "run", "python", "infer_model.py"]
