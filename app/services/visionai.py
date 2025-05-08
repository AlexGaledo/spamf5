from google.cloud import vision
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("vision_key")
vision_client = vision.ImageAnnotatorClient()

def analyzeImage(file):
    content = file.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    results = [{'description': label.description, 'score': label.score} for label in labels]

    return {'labels': results}
