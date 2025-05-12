import os
from flask import Blueprint, request, jsonify
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import io

voice_bp = Blueprint("voice_recog", __name__)

@voice_bp.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # Check if the request contains audio
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Read the FLAC audio file
    audio_content = audio_file.read()

    # Initialize Google Cloud Speech client
    client = speech.SpeechClient()

    # Setup the audio configuration for FLAC encoding
    audio = types.RecognitionAudio(content=audio_content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,  # Adjust based on your audio sample rate
        language_code="en-US"     # Set the language you want
    )

    # Perform speech recognition
    try:
        response = client.recognize(config=config, audio=audio)

        # If speech is recognized, return the transcriptions
        if response.results:
            transcriptions = [result.alternatives[0].transcript for result in response.results]
            return jsonify({"transcriptions": transcriptions}), 200
        else:
            return jsonify({"error": "No speech could be recognized"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

