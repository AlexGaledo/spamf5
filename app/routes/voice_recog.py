import os
from flask import Blueprint, request, jsonify
from google.cloud import speech
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

voice_bp = Blueprint("voice_recog", __name__)

@voice_bp.route("/", methods=["POST", "GET"])
def voice_recog():
    audio_file = request.files.get('file')
    if not audio_file:
        return jsonify({'response': 'requires uploaded file'}), 400

    try:
        # Convert the uploaded audio file to mono + 48000Hz using pydub
        original_audio = AudioSegment.from_file(audio_file)
        processed_audio = original_audio.set_channels(1).set_frame_rate(48000)

        # Save to temp WAV file (LINEAR16)
        with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            processed_audio.export(tmp_wav.name, format="wav")
            filepath = tmp_wav.name

        # Read the audio bytes
        with open(filepath, 'rb') as f:
            content = f.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,
            language_code="en-US",
        )
        client = speech.SpeechClient()

        # Transcribe
        response = client.recognize(config=config, audio=audio)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])

        return jsonify({"response": transcript}), 200

    except Exception as e:
        return jsonify({"response": "error occurred", "error": str(e)}), 500

    finally:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
