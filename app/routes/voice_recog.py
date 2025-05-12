import os
from flask import Blueprint, request, jsonify
from google.cloud import speech
from io import BytesIO

voice_bp = Blueprint("voice_recog", __name__)

@voice_bp.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get('file')
    if not file:
        return jsonify({'response': 'requires uploaded file'}), 400

    try:
        # Read the uploaded file content
        audio_content = file.read()

        # Create a client for the Speech-to-Text API
        client = speech.SpeechClient()

        # Prepare the audio data for Google Cloud
        audio_data = speech.RecognitionAudio(content=audio_content)

        # Configure the recognition settings
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Adjust if needed based on your audio file
            sample_rate_hertz=48000,  # Adjust according to the audio file sample rate
            language_code="en-US"
        )

        # Send the audio data for recognition
        response = client.recognize(config=config, audio=audio_data)

        # Extract the transcript
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])

        return jsonify({"transcript": transcript}), 200

    except Exception as e:
        return jsonify({"response": "error occurred", "error": str(e)}), 500
