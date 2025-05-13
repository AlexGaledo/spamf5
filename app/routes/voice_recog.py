
from flask import Blueprint, request, jsonify
from google.cloud import speech



voice_bp = Blueprint("voice_recog", __name__)

@voice_bp.route("/transcribe", methods=["POST","GET"])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    audio_file = request.files['file']
    audio_bytes = audio_file.read()

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return jsonify({'transcript': transcript})


