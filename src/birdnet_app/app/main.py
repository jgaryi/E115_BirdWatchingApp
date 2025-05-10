"""Bird species detection API using BirdNET and a custom classification model."""

from io import BytesIO
import tempfile
import os
from collections import defaultdict

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import joblib
import numpy as np
from birdnetlib.analyzer import Analyzer
from birdnetlib import Recording

app = FastAPI()

# Load our custom model
model = joblib.load('mlp_model_birdnet.pkl')

# Class label mapping for custom model
label_map = {
    1: "Doliornis sclateri",
    2: "Hapalopsittaca melanotis"
}

def preprocess_audio_bytes_to_wav_segment(audio_bytes):
    """Preprocess uploaded audio: pad to 3 seconds."""
    audio_io = BytesIO(audio_bytes)

    try:
        audio = AudioSegment.from_file(audio_io)  # auto-detect format
    except Exception as e:
        return {
            "error": "Unsupported or corrupt audio file.",
            "details": str(e)
        }

    target_duration_ms = 3000
    if len(audio) < target_duration_ms:
        silence = AudioSegment.silent(duration=target_duration_ms - len(audio))
        audio += silence
    else:
        audio = audio[:target_duration_ms]

    return audio

def analyze_birdnet_from_audio_segment(audio_segment, confidence_threshold=0.1):
    """Analyze a 3-second audio segments using BirdNET."""
    wav_io = BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(wav_io.read())
        temp_path = temp_file.name

    try:
        analyzer = Analyzer()
        recording = Recording(analyzer, temp_path)
        recording.analyze()

        species_confidences = defaultdict(list)
        for d in recording.detections:
            if d['confidence'] >= confidence_threshold:
                species_confidences[d['scientific_name']].append(d['confidence'])

        if not species_confidences:
            return None, temp_path

        avg_conf = {
            species: sum(confs) / len(confs)
            for species, confs in species_confidences.items()
        }

        top_species = max(avg_conf.items(), key=lambda x: x[1])
        return {
            "scientific_name": top_species[0],
            "average_confidence": round(top_species[1], 3)
        }, temp_path

    except Exception as e:
        return {"error": f"BirdNET analysis failed: {e}"}, temp_path

def classify_with_custom_model(audio_path):
    """Identify bird species from audio using transfer learning."""
    analyzer = Analyzer()
    recording = Recording(analyzer, audio_path)
    recording.extract_embeddings()
    embeddings = recording.embeddings

    for segment in embeddings:
        emb_vector = np.array(segment['embeddings']).reshape(1, -1)
        prediction = model.predict(emb_vector)[0]

        if prediction in label_map:
            return label_map[prediction]

    return "Species not identified"

def detect_species_from_audio(audio_bytes):
    """Full detection pipeline: preprocess, analyze with BirdNET, fallback to transfer learning if needed."""
    audio_segment = preprocess_audio_bytes_to_wav_segment(audio_bytes)
    if isinstance(audio_segment, dict) and "error" in audio_segment:
        return audio_segment

    birdnet_result, temp_path = analyze_birdnet_from_audio_segment(audio_segment)

    if birdnet_result is None or birdnet_result.get("average_confidence", 0) < 0.5:
        fallback_species = classify_with_custom_model(temp_path)
        os.remove(temp_path)
        return {
            "scientific_name": fallback_species,
            "source": "own custom model for local species"
        }

    os.remove(temp_path)
    return {
        "scientific_name": birdnet_result['scientific_name'],
        "average_confidence": birdnet_result['average_confidence'],
        "source": "birdnet"
    }

@app.post("/analyze-bird")
async def analyze(file: UploadFile = File(...)):
    """API endpoint to analyze uploaded audio and identify bird species."""
    audio_bytes = await file.read()
    result = detect_species_from_audio(audio_bytes)

    if isinstance(result, dict) and result.get("error"):
        return JSONResponse(status_code=400, content=result)

    return result
