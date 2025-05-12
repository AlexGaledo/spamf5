import os
from flask import Blueprint, request, jsonify
from google.cloud import speech

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
        audio = speech.RecognitionAudio(content=audio_content)

        # Configure recognition settings (accepts LINEAR16 WAV mono 16-bit 16kHz)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            audio_channel_count=1
        )

        # Perform the transcription
        response = client.recognize(config=config, audio=audio)

        transcript = " ".join(result.alternatives[0].transcript for result in response.results)
        return jsonify({"transcript": transcript}), 200

    except Exception as e:
        return jsonify({"response": "error occurred", "error": str(e)}), 500
