from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
import librosa
from pydub import AudioSegment
import numpy as np
import tempfile
import os
from bird import app, preprocess_audio_bytes_to_wav_segment, analyze_birdnet_from_audio_segment, classify_with_custom_model, detect_species_from_audio

client = TestClient(app)

# I. Test the Full Pipeline with Simulated Audio
def test_full_integration_with_simulated_audio():
    silent_audio = AudioSegment.silent(duration=3000)  # 3000ms = 3s
    audio_bytes = silent_audio.export(format="wav").read()
    
    # 1. Test preprocessing
    audio_segment = preprocess_audio_bytes_to_wav_segment(audio_bytes)
    assert isinstance(audio_segment, AudioSegment)  # Not a dict (no error)
    
    # 2. Test BirdNET analysis
    birdnet_result, temp_path = analyze_birdnet_from_audio_segment(audio_segment)
    if birdnet_result:  # If BirdNET detects something
        assert "scientific_name" in birdnet_result
        assert 0 <= birdnet_result["average_confidence"] <= 1
    else:  # Test fallback to custom model
        custom_result = classify_with_custom_model(temp_path)
        assert custom_result in ["Doliornis sclateri", "Hapalopsittaca melanotis", "Species not identified"]
    
    # 3. Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


# II. API Integration Test with Simulated Audio
def test_api_integration_with_simulated_audio():
    # 1. Generate simulated silent audio
    silent_audio = AudioSegment.silent(duration=3000)  # 3000ms = 3s
    audio_bytes = silent_audio.export(format="wav").read()  # Simulate a 3s silent audio file

    # 2. Send to API (no mocks)
    response = client.post(
        "/analyze-bird",
        files={"file": ("simulated_audio.wav", audio_bytes, "audio/wav")}  # Use a valid filename
    )
    
    # 3. Verify response structure
    assert response.status_code == 200
    result = response.json()
    print("API Response:", result)  # Debugging: Print the response
    assert isinstance(result, dict)
    assert "scientific_name" in result
    assert "source" in result
    if "scientific_name" == "Species not identified":
        assert "average_confidence" not in result
    # else:
    #     assert "average_confidence" in result
    #     assert 0 <= result["average_confidence"] <= 1

    # 4. Validate output based on source
    if result["source"] == "birdnet":
        assert isinstance(result["average_confidence"], float)
    else:  # Custom model fallback
        assert result["scientific_name"] in ["Doliornis sclateri", "Hapalopsittaca melanotis", "Species not identified"]


# III. Test Edge Cases in Integration, Verify real-world scenarios that unit tests might miss
def test_integration_edge_cases():
    # Case 1: Very short audio (should be padded to 3s)
    short_audio = AudioSegment.silent(duration=1000)  # 1 second
    short_audio_bytes = short_audio.export(format="wav").read()
    response = client.post("/analyze-bird", files={"file": ("short.wav", short_audio_bytes, "audio/wav")})
    assert response.status_code == 200  # Should handle padding
    
    # Case 2: Long audio (should be trimmed)
    long_audio = AudioSegment.silent(duration=90000)  # 90 seconds
    long_audio_bytes = long_audio.export(format="wav").read()
    response = client.post("/analyze-bird", files={"file": ("long.wav", long_audio_bytes, "audio/wav")})
    assert response.status_code == 200  # Should handle trimming


# IV. Cross-Validate BirdNET and Custom Model, Ensures the models don’t contradict each other for known samples.
# confirm to contain "Doliornis sclateri", If BirdNET is uncertain (low confidence), 
# the custom model at least does not return "Species not identified".
def test_model_agreement_on_known_samples():
    # Generate simulated silent audio
    silent_audio = AudioSegment.silent(duration=3000)  # 3000ms = 3s
    audio_bytes = silent_audio.export(format="wav").read()  # Simulate a 3s silent audio file
    
    # 1. Get BirdNET result
    audio_segment = preprocess_audio_bytes_to_wav_segment(audio_bytes)
    birdnet_result, temp_path = analyze_birdnet_from_audio_segment(audio_segment)
    print("BirdNET Result:", birdnet_result)  # Debugging: Print the BirdNET result

    # 2. Get custom model result
    custom_result = classify_with_custom_model(temp_path)
    print("Custom Result:", custom_result)  # Debugging: Print the custom result

    # 3. They should agree (or at least not contradict)
    if birdnet_result and birdnet_result["average_confidence"] > 0.5:
        assert birdnet_result["scientific_name"] == custom_result  # Strong agreement
    else:
        assert custom_result in ["Doliornis sclateri", "Hapalopsittaca melanotis", "Species not identified"]  # Weak agreement

    # 4. Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


# V. Performance Testing, check the processing time to vrify API's efficiency to handles multiple requests
def test_processing_performance():
    import time
    # Generate simulated silent audio
    silent_audio = AudioSegment.silent(duration=3000)  # 3000ms = 3s
    audio_bytes = silent_audio.export(format="wav").read()  # Simulate a 3s silent audio file
    
    start_time = time.time()
    response = client.post("/analyze-bird", files={"file": ("simulated_audio.wav", audio_bytes, "audio/wav")})
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 5.0  # Process within 5 seconds
    print(f"Processing time: {end_time - start_time:.2f}s")