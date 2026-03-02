import os
import time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv
from PIL import Image
import io
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Define retry decorator for 429s
def retry_on_quota(func):
    return retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=10, min=20, max=60),
        retry=retry_if_exception_type(ClientError),
        before_sleep=lambda retry_state: print(f"Quota exceeded. Retrying in {retry_state.next_action.sleep}s... (Attempt {retry_state.attempt_number})")
    )(func)

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


@retry_on_quota
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
        model="gemini-2.0-flash",
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"),
            """Transcribe this patient's spoken input accurately. 
        Preserve all medical terms, symptom descriptions, and personal details mentioned.
        Format as natural text."""
        ]
    )
    
    # Rate limiting for Free Tier (10 RPM) - Increased to protect 4-agent crew quota
    print("Waiting for quota (long wait)...")
    time.sleep(25)

    if converted_path != audio_file_path:
        os.remove(converted_path)

    return response.text


@retry_on_quota
def analyze_document_image(image_file_path):
    """Analyzes a medical document image using Gemini."""
    # Detect mime type
    ext = image_file_path.rsplit(".", 1)[-1].lower()
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "pdf": "application/pdf", "gif": "image/gif", "webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
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
    
    # Rate limiting for Free Tier (10 RPM) - Increased to protect 4-agent crew quota
    print("Waiting for quota (long wait)...")
    time.sleep(25)

    return response.text


@retry_on_quota
def analyze_symptom_image(image_path):
    """Analyzes an image of a symptom (wound, rash, etc.) using Gemini."""
    ext = image_path.rsplit(".", 1)[-1].lower()
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
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
    
    # Rate limiting for Free Tier (10 RPM) - Increased to protect 4-agent crew quota
    print("Waiting for quota (long wait)...")
    time.sleep(25)

    return response.text
