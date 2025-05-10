FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (ffmpeg is required by pydub for mp3/etc.)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install pipenv and project dependencies
RUN pip install --upgrade pip pipenv

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system

COPY app /app/app
COPY mlp_model_birdnet.pkl /app/mlp_model_birdnet.pkl

EXPOSE 9090

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]
