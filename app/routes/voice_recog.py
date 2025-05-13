from flask import Blueprint, request, jsonify
from google.cloud import speech
from pydub import AudioSegment
import io

voice_bp = Blueprint("voice_recog", __name__)

@voice_bp.route("/transcribe", methods=["POST", "GET"])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    audio_file = request.files['file']
    audio_bytes = audio_file.read()

    # Use pydub to check the sample rate and format of the uploaded audio file
    audio = AudioSegment.from_wav(io.BytesIO(audio_bytes))
    sample_rate = audio.frame_rate
    channels = audio.channels

    # Ensure it's mono (Google Speech requires mono audio)
    if channels != 1:
        return jsonify({'error': 'Audio file must be mono'}), 400

    # Initialize the Speech client
    client = speech.SpeechClient()
    audio_content = speech.RecognitionAudio(content=audio_bytes)

    # Set the config with the detected sample rate
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,  # Set sample rate automatically
        language_code="en-US",
    )

    try:
        response = client.recognize(config=config, audio=audio_content)

        # Extract the transcript
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return jsonify({'transcript': transcript})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
