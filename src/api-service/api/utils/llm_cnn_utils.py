import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
import base64
import io
import json
import requests
import zipfile
import numpy as np
from PIL import Image
from pathlib import Path
import tempfile
from tempfile import TemporaryDirectory
import traceback
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import Model
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from fastapi import UploadFile
# from vertexai.generative_models import GenerativeModel, ChatSession, Part
from .llm_agent_utils import (
    chat_sessions,
    create_chat_session,
    generate_chat_response,
    rebuild_chat_session
)

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
# GENERATIVE_MODEL = "gemini-1.5-flash-002"

# CNN Model details
AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent/experiments"
best_model = None
best_model_id = None
cnn_model = None
data_details = None
image_width = 224
image_height = 224
num_channels = 3

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.1,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}



def load_cnn_model():
    analyzer = Analyzer()
    return analyzer


audio_path = "api/utils/acoustic_data_Pipile cumanensis_XC128802 - Blue-throated Piping Guan - Pipile cumanensis.mp3" #if you want to test the model within the CLI, can put an audio file in this path

def load_preprocess_image_from_path(audio_path): #audio_path - "XC333241.mp3"
    # Load the CNN Model
    analyzer = load_cnn_model() 

    
    recording = Recording(
        analyzer,
        audio_path,
        )
    return recording


def make_prediction(audio_path=audio_path):

    # Load & preprocess
    recording = load_preprocess_image_from_path(audio_path)

    # Make prediction
    recording.analyze()
    # print(recording.detections)

    from collections import defaultdict

    def calculate_average_confidence(bird_data):
        # Step 1: Group confidence values by bird species
        species_confidences = defaultdict(list)
        for entry in bird_data:
            species = entry['scientific_name']
            confidence = entry['confidence']
            species_confidences[species].append(confidence)
        
        # Step 2: Calculate the average confidence for each species
        average_confidences = []
        for species, confidences in species_confidences.items():
            avg_confidence = sum(confidences) / len(confidences)
            average_confidences.append({
                'scientific_name': species,
                'average_confidence': avg_confidence
            })
            
        # Step 3: Sort by average confidence (descending order)
        average_confidences.sort(key=lambda x: x['average_confidence'], reverse=True)
        
        return average_confidences
    results = calculate_average_confidence(recording.detections)
    confidence_threshold = 0.3
    species_in_audio = [d for d in results if d['average_confidence'] > confidence_threshold]
    print("Species in audio:", species_in_audio)
    if len(species_in_audio) == 0:
        return {
            "prediction_label": "No species detected",
            "accuracy": 0.0
        }

    return species_in_audio



def predict_bird_from_base64_string(base64_str: str, mime_type: str = "audio/mp3") -> str:
    try:
        if ',' in base64_str:
            _, base64_data = base64_str.split(",", 1)
        else:
            base64_data = base64_str

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(base64.b64decode(base64_data))
            tmp_path = tmp.name

        prediction = make_prediction(audio_path=tmp_path)
        if isinstance(prediction, list) and prediction:
            top = prediction[0]
            return f"The uploaded audio likely contains the species *{top['scientific_name']}* with average confidence {top['average_confidence']:.2f}., restate this 'The uploaded audio is the sound of *{top['scientific_name']}*', then proceed to tell me more about the species."
        return "Restate 'No bird species were confidently detected in the audio.'"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


def generate_chat_response1(chat_session, message):
    content = message.get("content", "").strip()
    
    if not content:
        audio_b64 = message.get("audio", "")
        if not audio_b64:
            raise HTTPException(status_code=400, detail="Provide either message text or audio.")
        message["content"] = predict_bird_from_base64_string(audio_b64)

    return generate_chat_response(chat_session, message)



def rebuild_chat_session1(chat_history: List[Dict]):
    # Add transformation for cnn role since agent expects user/model roles
    adjusted_history = []
    for message in chat_history:
        if message["role"] == "cnn":
            message["role"] = "user"
            message["content"] = f"We have already identified the audio as {message['results']['prediction_label']}"
        adjusted_history.append(message)
    
    return rebuild_chat_session(adjusted_history)


