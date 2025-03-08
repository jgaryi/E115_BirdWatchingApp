# Use the official python runtime as a parent image
FROM python:3.9-slim-buster

# Tell pipenv where the shell is. 
# This allows us to use "pipenv shell" as a container entry point.
ENV PYENV_SHELL=/bin/bash

# Ensure we have an up-to-date baseline and install any OS dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash app

# Set the working directory to /app
WORKDIR /app

# Install pipenv
RUN pip install pipenv
# RUN pip install numba
# RUN pip install scipy
# RUN pip install tensorflow==2.15.0
# RUN pip install birdnetlib

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

RUN pipenv sync

# Source code
ADD . /app

# Entry point
ENTRYPOINT ["/bin/bash"]

# Get into the pipenv shell
CMD ["-c", "pipenv shell"]
#CMD ["python", "Species_Prediction.py"]
