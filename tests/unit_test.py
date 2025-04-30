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

# Dynamically locate the test.mp3 file
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(current_dir, "test.mp3")

# Check if the file exists
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"Audio file not found at {audio_path}")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()  # Returns bytes object


# I. Audio duration test cases
def test_preprocess_short_audio():
    """Test if the audio is less than 3 seconds"""
    duration = librosa.get_duration(path=audio_path)
    print(f"Audio duration: {duration} seconds")
    assert duration >= 3  # Should be longer than 3 seconds

def test_preprocess_long_audio():
    """Test if the audio is longer than 60 seconds"""
    duration = librosa.get_duration(path=audio_path)
    print(f"Audio duration: {duration} seconds")
    assert duration <= 90  # Should be less than 90 seconds


# II. Utility functions for testing - Create digital silence and audio file for testing
def generate_silent_audio(duration_ms=3000):
    """Generate silent audio segment for testing"""
    return AudioSegment.silent(duration=duration_ms)

def create_test_audio_file(duration_ms=3000):
    """Create a temporary test audio file"""
    audio = generate_silent_audio(duration_ms)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio.export(f.name, format="wav")
        return f.name


# III. Test birdnet analysis and classification
# use MagicMock to mock the Recording class and simulate its behavior and return values
# instead of using the actual audio file since the test should be independent of external files
# Test case for birdnet with successful detection
@patch('bird.Analyzer')
@patch('bird.Recording')
def test_analyze_birdnet_success(mock_recording, mock_analyzer):
    """Test successful bird detection"""
    # Setup mocks
    mock_recording_instance = MagicMock()
    mock_recording_instance.detections = [
        {'scientific_name': 'Testus birdius', 'confidence': 0.8},
        {'scientific_name': 'Testus birdius', 'confidence': 0.9}
    ]
    mock_recording.return_value = mock_recording_instance
    
    audio_segment = generate_silent_audio(3000)
    result, temp_path = analyze_birdnet_from_audio_segment(audio_segment)
    print("Test result:", result)
    assert result["scientific_name"] == "Testus birdius"
    assert result["average_confidence"] == 0.85
    os.remove(temp_path)

# Test cases for birdnet with no detection
@patch('bird.Analyzer')
@patch('bird.Recording')
def test_analyze_birdnet_no_detection(mock_recording, mock_analyzer):
    """Test case with no bird detection"""
    mock_recording_instance = MagicMock()
    mock_recording_instance.detections = []
    mock_recording.return_value = mock_recording_instance
    
    audio_segment = generate_silent_audio(3000)
    result, temp_path = analyze_birdnet_from_audio_segment(audio_segment)
    
    assert result is None
    os.remove(temp_path)


# IV. Testing Custom Model Classification 
# Test cases for birdnet with low confidence and switch to custom model
# Test case for classify_with_custom_model with known species
@patch('bird.Analyzer')
@patch('bird.Recording')
@patch('bird.model.predict')
def test_classify_known_species(mock_predict, mock_recording, mock_analyzer):
    """Test classification of known species"""
    # Setup mock embeddings
    mock_recording_instance = MagicMock()
    mock_recording_instance.embeddings = [{'embeddings': [0.1, 0.2, 0.3]}]
    mock_recording.return_value = mock_recording_instance
    
    # Mock model prediction
    mock_predict.return_value = [1]  # Doliornis sclateri, change value to 2 for Hapalopsittaca melanotis
    
    temp_path = create_test_audio_file()
    result = classify_with_custom_model(temp_path)
    
    assert result == "Doliornis sclateri"
    os.remove(temp_path)

# Test cases for classify_with_custom_model with unknown species
@patch('bird.Analyzer')
@patch('bird.Recording')
@patch('bird.model.predict')
def test_classify_unknown_species(mock_predict, mock_recording, mock_analyzer):
    """Test classification when species is unknown"""
    mock_recording_instance = MagicMock()
    mock_recording_instance.embeddings = [{'embeddings': [0.1, 0.2, 0.3]}]
    mock_recording.return_value = mock_recording_instance
    
    mock_predict.return_value = [99]  # Unknown species
    
    temp_path = create_test_audio_file()
    result = classify_with_custom_model(temp_path)
    
    assert result == "Species not identified"
    os.remove(temp_path)


# Test full detection pipeline
# test case with successful detection using BirdNET
@patch('bird.analyze_birdnet_from_audio_segment')
@patch('bird.classify_with_custom_model')
def test_detect_species_birdnet_success(mock_custom, mock_birdnet):
    """Test primary path using BirdNET"""
    # Mock BirdNET result to match the expected structure
    mock_birdnet.return_value = (
        {"scientific_name": "Birdnet result", "average_confidence": 0.9},
        create_test_audio_file()
    )
    
    # Call the function under test
    result = detect_species_from_audio(audio_bytes)
    
    # Debugging: Print the result to verify its structure
    print("Test result:", result)
    
    # # Check if the result contains an error
    # if "error" in result:
    #     pytest.fail(f"Function returned an error: {result['error']}")

    # Assert the result contains the expected keys and values
    assert result["source"] == "birdnet"
    assert result["scientific_name"] == "Birdnet result"
    assert result["average_confidence"] == 0.9

# Test cases with fallback to custom model
@patch('bird.analyze_birdnet_from_audio_segment')
@patch('bird.classify_with_custom_model')
def test_detect_species_fallback(mock_custom, mock_birdnet):
    """Test fallback to custom model"""
    mock_birdnet.return_value = (None, create_test_audio_file())
    mock_custom.return_value = "Custom result"
    
    result = detect_species_from_audio(audio_bytes)
    assert result["source"] == "own custom model for local species"
    assert result["scientific_name"] == "Custom result"


# Test API endpoint with valid audio - successful request
def test_api_endpoint_success():
    """Test successful API request"""
    test_audio = generate_silent_audio(3000).export(format="wav").read()
    
    with patch('bird.detect_species_from_audio') as mock_detect:
        mock_detect.return_value = {
            "scientific_name": "Test bird",
            "average_confidence": 0.95,
            "source": "birdnet"
        }
        
        response = client.post(
            "/analyze-bird",
            files={"file": ("test.wav", test_audio, "audio/wav")}
        )
        
        assert response.status_code == 200
        assert response.json()["scientific_name"] == "Test bird"


# Test API endpoint with invalid audio - failed request
def test_api_endpoint_invalid_audio():
    """Test API with invalid audio"""
    with patch('bird.preprocess_audio_bytes_to_wav_segment') as mock_preprocess:
        mock_preprocess.return_value = {
            "error": "Invalid audio",
            "details": "Test error"
        }
        
        response = client.post(
            "/analyze-bird",
            files={"file": ("test.wav", b"invalid", "audio/wav")}
        )
        
        assert response.status_code == 400
        assert "Invalid audio" in response.json()["error"]