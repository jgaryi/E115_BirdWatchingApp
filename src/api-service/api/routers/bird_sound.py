"""FastAPI router for accessing bird sounds and associated images."""

import os
import glob
import json
import traceback
from typing import Optional
import requests
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Initialize FastAPI router
router = APIRouter()

# Get data from bucket
BUCKET_URL = "https://storage.googleapis.com/birdwatching_app/"

FILES = [
    "bird_sounds/9f2b7e84-5623-4029-bcfd-f99f2d7611e8.json",
    "bird_sounds/184a8951-9a41-4331-acf2-fbba23b88a62.json",
    "bird_sounds/2956ab09-3218-4ad2-bdef-fcccaf8b0008.json",
    "bird_sounds/a04bb69e-f217-4e30-995b-cc1beddcc79e.json",
    "bird_sounds/assets/9f2b7e84-5623-4029-bcfd-f99f2d7611e8-EN.mp3",
    "bird_sounds/assets/184a8951-9a41-4331-acf2-fbba23b88a62-EN.mp3",
    "bird_sounds/assets/2956ab09-3218-4ad2-bdef-fcccaf8b0008-EN.mp3",
    "bird_sounds/assets/a04bb69e-f217-4e30-995b-cc1beddcc79e-EN.mp3"
]

# Loop through each file
for file_path in FILES:
    local_path = os.path.join(".", file_path)  # Local mirror of GCS path

    # Skip if already downloaded
    if os.path.exists(local_path):
        logger.debug(f"Skipping {file_path} (already exists)")
        continue

    # Make sure the local folder exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Build the public URL to the file
    url = f"{BUCKET_URL}{file_path}"
    logger.debug(f"Downloading {file_path}...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.debug(f"Failed to download {file_path}: {e}")
        continue

    with open(local_path, "wb") as file_obj:
        file_obj.write(response.content)
    logger.debug(f"Saved: {local_path}")

DATA_FOLDER = "bird_sounds"

# List all bird sound metadata
@router.get("/")
async def get_bird_sounds(limit: Optional[int] = None):
    """
    Return a list of bird sound metadata entries.
    """
    bird_sounds = []
    data_files = glob.glob(os.path.join(DATA_FOLDER, "*.json"))
    for file_path in data_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as sound_file:
                sound_data = json.load(sound_file)
                bird_sounds.append(sound_data)
        except Exception as e:
            logger.debug(f"Error loading bird_sounds from {file_path}: {str(e)}")
            traceback.print_exc()

    # Sort metadata by datetime (most recent first)
    bird_sounds.sort(key=lambda x: x.get('dts', 0), reverse=True)

    # Return limited subset if limit specified
    if limit:
        return bird_sounds[:limit]

    return bird_sounds

# Get a specific bird sound entry by ID
@router.get("/{bird_sound_id}")
async def get_bird_sound(bird_sound_id: str):
    """
    Retrieve a specific bird sound metadata entry by ID.
    """
    file_path = os.path.join(DATA_FOLDER, f"{bird_sound_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Bird sound not found")

    with open(file_path, 'r', encoding='utf-8') as sound_file:
        bird_sound = json.load(sound_file)

    return bird_sound

# Serve audio file for a bird sound
@router.get("/audio/{audio_name}")
async def get_bird_sound_audio(audio_name: str):
    """
    Serve the MP3 file for a specific bird sound.
    """
    try:
        audio_path = os.path.join(DATA_FOLDER, "assets", audio_name)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Bird sound audio not found")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Disposition": f"attachment; filename={audio_name}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
