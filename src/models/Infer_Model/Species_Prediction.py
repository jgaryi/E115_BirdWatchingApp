from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime


def extract_values(dict_list, key):
    """Extracts the values of a specific key from a list of dictionaries."""
    return [dictionary[key] for dictionary in dict_list if key in dictionary]


# Load and initialize the BirdNET-Analyzer models.
analyzer = Analyzer()

recording = Recording(
    analyzer,
    'XC178.mp3',
)

recording.analyze()

# Get the prediction of species and their confidence values.
pred = recording.detections
print(pred)

confidences = extract_values(pred, "confidence")
label = extract_values(pred, "label")
avg_confidence = sum(confidences)/len(confidences)
print(f"The record contains song of bird -- {label[0]} with confidence {avg_confidence}")
print("it works")