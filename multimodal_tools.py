import os
import base64
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# 🎤 AUDIO TRANSCRIPTION — Whisper (Local, Free)
# ─────────────────────────────────────────────
def transcribe_audio(audio_file_path):
    """
    Transcribes patient voice input using OpenAI Whisper locally.
    No API key needed. Runs 100% on your machine.
    """
    try:
        import whisper
    except ImportError:
        raise ImportError("Please run: pip install openai-whisper")

    print(f"Loading Whisper model...")
    model = whisper.load_model("base")  # options: tiny, base, small, medium, large

    print(f"Transcribing audio: {audio_file_path}")
    result = model.transcribe(audio_file_path)
    transcript = result["text"].strip()

    print(f"Transcription complete: {transcript[:100]}...")
    return transcript


# ─────────────────────────────────────────────
# 📄 DOCUMENT ANALYSIS — Groq Vision (Free)
# ─────────────────────────────────────────────
def analyze_document_image(image_file_path):
    """
    Analyzes a medical document image using Groq Vision (Llama 4 Scout).
    Free tier with generous limits.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("Please run: pip install groq")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Detect mime type
    ext = image_file_path.rsplit(".", 1)[-1].lower()
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "pdf": "image/jpeg"  # for PDFs, convert first page to image if needed
    }
    mime_type = mime_map.get(ext, "image/jpeg")

    # Read and encode image
    with open(image_file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    print(f"Analyzing document with Groq Vision: {image_file_path}")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": """Analyze this medical document/image and extract ALL information including:
- Patient name and details
- Medications, dosages, and instructions
- Diagnoses and conditions
- Lab results and values
- Doctor's notes and recommendations
- Dates and visit information
- Any other clinically relevant information

Be thorough and precise. Include all numbers, units, and medical terminology."""
                    }
                ]
            }
        ],
        max_tokens=1024
    )

    result = response.choices[0].message.content
    print(f"Document analysis complete.")
    return result


# ─────────────────────────────────────────────
# 🩺 SYMPTOM IMAGE ANALYSIS — Groq Vision (Free)
# ─────────────────────────────────────────────
def analyze_symptom_image(image_path):
    """
    Analyzes an image of a symptom (wound, rash, etc.) using Groq Vision.
    Free tier with generous limits.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("Please run: pip install groq")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    ext = image_path.rsplit(".", 1)[-1].lower()
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    print(f"Analyzing symptom image with Groq Vision: {image_path}")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": """Analyze this clinical image and describe:
- What is visible (wound, rash, swelling, etc.)
- Location on body (if determinable)
- Approximate size/extent
- Color, texture, appearance characteristics
- Any concerning features that should be flagged for the doctor

Be clinically descriptive and objective."""
                    }
                ]
            }
        ],
        max_tokens=1024
    )

    result = response.choices[0].message.content
    print(f"Symptom image analysis complete.")
    return result
