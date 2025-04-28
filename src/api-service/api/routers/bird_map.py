"""FastAPI router for accessing bird maps and associated images."""

import os
import glob
import json
import traceback
from typing import Optional
import requests

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Initialize FastAPI router
router = APIRouter()

# Get data from bucket
BUCKET_URL = "https://storage.googleapis.com/birdwatching_app/"

FILES = [
    "bird_maps/9f2b7e84-2176-4029-bcfd-f99f2d7611e8.json",
    "bird_maps/59c066b0-4765-4239-aa9b-c31d212d9697.json",
    "bird_maps/78ff70af-c678-486c-876f-9a588a567385.json",
    "bird_maps/assets/mapbirdbiod.jpg",
    "bird_maps/assets/mapbirddef.jpg",
    "bird_maps/assets/mapbirdlocation.jpg"
]

# Loop through each file
for file_path in FILES:
    local_path = os.path.join(".", file_path)

    # Skip if already downloaded
    if os.path.exists(local_path):
        print(f"Skipping {file_path} (already exists)")
        continue

    # Make sure the local folder exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Build the public URL to the file
    url = f"{BUCKET_URL}{file_path}"
    print(f"Downloading {file_path}...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to download {file_path}: {e}")
        continue

    with open(local_path, "wb") as file_obj:
        file_obj.write(response.content)
    print(f"Saved: {local_path}")

DATA_FOLDER = "bird_maps"

# Get a list of bird maps
@router.get("/")
async def get_bird_maps(limit: Optional[int] = None):
    """
    Fetch a list of all bird map metadata from local JSON files.
    """
    bird_maps = []

    data_files = glob.glob(os.path.join(DATA_FOLDER, "*.json"))

    for file_path in data_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                chat_data = json.load(json_file)
                bird_maps.append(chat_data)
        except Exception as e:
            print(f"Error loading chat history from {file_path}: {str(e)}")
            traceback.print_exc()

    bird_maps.sort(key=lambda x: x.get('dts', 0), reverse=True)

    if limit:
        return bird_maps[:limit]

    return bird_maps

# Get a single bird map by ID
@router.get("/{bird_map_id}")
async def get_bird_map(bird_map_id: str):
    """
    Fetch a single bird map by its unique identifier (file name).
    """
    file_path = os.path.join(DATA_FOLDER, f"{bird_map_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Bird map not found")

    with open(file_path, 'r', encoding='utf-8') as json_file:
        bird_map = json.load(json_file)

    return bird_map

# Get an image asset associated with a bird map
@router.get("/image/{image_name}")
async def get_bird_map_image(image_name: str):
    """
    Serve a static image file associated with a bird map.
    """
    content_type = "application/octet-stream"
    image_path = os.path.join(DATA_FOLDER, "assets", image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        path=image_path,
        media_type=content_type
    )
