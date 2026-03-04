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
# 📄 DOCUMENT ANALYSIS — PDF, Word, Text
# ─────────────────────────────────────────────
def analyze_document_image(file_path):
    """
    Analyzes a medical document (PDF, Word, or Text) by extracting text
    and summarizing it using Groq.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("Please run: pip install groq")

    ext = file_path.rsplit(".", 1)[-1].lower()
    text = ""

    try:
        if ext == 'pdf':
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif ext in ['doc', 'docx']:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        else:
            return f"Unsupported file extension: {ext}"
    except Exception as e:
        return f"Error extracting text from {ext} file: {str(e)}"

    if not text.strip():
        return "No text could be extracted from the document."

    print(f"Analyzing extracted text from {ext} with Groq...")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Using a powerful text model for clinical analysis
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": "You are a Clinical Document Analyst. Your goal is to extract structured medical information from raw document text."
            },
            {
                "role": "user",
                "content": f"""Analyze this extracted medical document text and isolate:
- Patient info
- Medications & Dosages
- Diagnoses
- Lab values
- Next steps/Recommendations

Text:
{text[:8000]}""" # Limit to 8000 chars for safety
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
