import base64
import os
from google import genai
from google.genai import types
import requests

# Step 1: Decode the base64-encoded JSON key stored in the environment variable
encoded_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not encoded_key:
    raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

# Step 2: Decode the base64 string and write it to a temporary file
decoded_key = base64.b64decode(encoded_key)

# Save the key to a temporary location (Render uses /tmp directory for temp files)
key_file_path = '/tmp/google-key.json'

with open(key_file_path, 'wb') as key_file:
    key_file.write(decoded_key)

# Step 3: Set the environment variable for Google Cloud SDK
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path

# Initialize the client
client = genai.Client(
    vertexai=True,
    project="baybay-459214",
    location="us-central1",
)


def generate_with_image(text, image_url):
    # Fetch image from the URL
    with open(image_url, "rb") as f:
        image_bytes = f.read()

    # Prepare the multimodal content
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=text),
                types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_bytes))
            ]
        )
    ]

    # Configure generation
    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"]
    )

    # Generate response
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-pro-preview-05-06",
        contents=contents,
        config=config,
    ):
        print(chunk.text, end="")
        full_response += chunk.text

    return full_response
