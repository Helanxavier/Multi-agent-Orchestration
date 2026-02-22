import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def wait_for_active_file(file_name):
    """Waits for an uploaded file to be in the ACTIVE state."""
    for _ in range(30):
        file = client.files.get(name=file_name)
        if file.state.name == "ACTIVE":
            return file
        if file.state.name == "FAILED":
            raise Exception(f"File failed to process: {file.error}")
        time.sleep(1)
    raise Exception(f"File timed out waiting to become ACTIVE")


def convert_to_mp3(input_path):
    """Converts audio to mp3 using pydub."""
    from pydub import AudioSegment
    output_path = input_path.rsplit(".", 1)[0] + ".mp3"
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="mp3")
    return output_path


def transcribe_audio(audio_file_path):
    """Transcribes patient voice input using Gemini."""
    # Convert to mp3 if needed
    if not audio_file_path.endswith(".mp3"):
        converted_path = convert_to_mp3(audio_file_path)
    else:
        converted_path = audio_file_path

    with open(converted_path, "rb") as f:
        audio_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"),
            """Transcribe this patient's spoken input accurately. 
        Preserve all medical terms, symptom descriptions, and personal details mentioned.
        Format as natural text."""
        ]
    )

    if converted_path != audio_file_path:
        os.remove(converted_path)

    return response.text


def analyze_document_image(image_path):
    """Analyzes a medical document image using Gemini."""
    # Detect mime type
    ext = image_path.rsplit(".", 1)[-1].lower()
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "pdf": "application/pdf", "gif": "image/gif", "webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            """Analyze this medical document/image and extract ALL information including:
        - Patient name and details
        - Medications, dosages, and instructions
        - Diagnoses and conditions
        - Lab results and values
        - Doctor's notes and recommendations
        - Dates and visit information
        - Any other clinically relevant information
        
        Be thorough and precise. Include all numbers, units, and medical terminology."""
        ]
    )

    return response.text


def analyze_symptom_image(image_path):
    """Analyzes an image of a symptom (wound, rash, etc.) using Gemini."""
    ext = image_path.rsplit(".", 1)[-1].lower()
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            """Analyze this clinical image and describe:
        - What is visible (wound, rash, swelling, etc.)
        - Location on body (if determinable)
        - Approximate size/extent
        - Color, texture, appearance characteristics
        - Any concerning features that should be flagged for the doctor
        
        Be clinically descriptive and objective."""
        ]
    )

    return response.text
