# IntakeAI — Patient Intake Assistant
### Comprehensive Project Documentation

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Project Structure](#3-project-structure)
4. [Backend — File-by-File Reference](#4-backend--file-by-file-reference)
5. [Frontend — index.html](#5-frontend--indexhtml)
6. [AI Workflow (CrewAI Agents)](#6-ai-workflow-crewai-agents)
7. [API Reference](#7-api-reference)
8. [Setup & Installation](#8-setup--installation)
9. [Environment Variables](#9-environment-variables)
10. [Running the Application](#10-running-the-application)
11. [Known Issues & Troubleshooting](#11-known-issues--troubleshooting)
12. [Technology Stack](#12-technology-stack)

---

## 1. Project Overview

**IntakeAI** is an AI-powered patient intake assistant designed for healthcare settings. It collects patient information through a rich web interface — including typed text, voice recordings, medical documents, and symptom photos — and uses Google Gemini AI + CrewAI agents to automatically generate a structured, professional intake form ready for the doctor.

### Key Features
- 🎙️ **Voice recording** — patients can speak their symptoms
- 📄 **Document upload** — prescriptions, lab reports, medical records (PDF/images)
- 📸 **Symptom photo upload** — for visual conditions (wounds, rashes, etc.)
- 🤖 **Multi-agent AI pipeline** — 4 specialized AI agents process and synthesize data
- 📋 **Structured intake form** — generated in Markdown, rendered in the browser
- 🖨️ **PDF export** — via browser print dialog
- 🔒 **HIPAA-compliant design** — secure data handling

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER (User)                        │
│                  http://localhost:8080                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  Screen 1    │  │    Screen 2       │  │   Screen 3    │  │
│  │  Input Form  │→ │   Processing      │→ │    Result     │  │
│  │  (Page 2)    │  │   (Page 1)        │  │   (Page 3)    │  │
│  └──────────────┘  └──────────────────┘  └───────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ POST /intake (multipart/form-data)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (main.py)                   │
│                     Port: 8080                               │
│                                                              │
│  1. Transcribe audio  →  multimodal_tools.transcribe_audio() │
│  2. Analyze documents →  multimodal_tools.analyze_document() │
│  3. Analyze images    →  multimodal_tools.analyze_symptom()  │
│  4. Run CrewAI        →  4 agents, 4 tasks                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Google Gemini AI (via two SDKs)                 │
│                                                              │
│  • google-genai SDK   → multimodal (audio, images, docs)    │
│  • langchain-google-genai → CrewAI agent LLM calls          │
│                                                              │
│  Model: gemini-2.0-flash-lite                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Project Structure

```
files/
├── main.py                # FastAPI app — API routes, orchestration
├── agents.py              # CrewAI agent definitions (4 agents)
├── tasks.py               # CrewAI task definitions (4 tasks)
├── multimodal_tools.py    # Gemini multimodal functions (audio, images)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (GOOGLE_API_KEY)
├── static/
│   └── index.html         # Single-page frontend (all 3 screens)
├── temp_uploads/          # Temporary storage for uploaded files
├── App.jsx                # (Legacy React component — not used)
├── App.css                # (Legacy React styles — not used)
└── package.json           # (Legacy React config — not used)
```

> **Note:** `App.jsx`, `App.css`, and `package.json` are legacy files from an earlier React-based frontend. The current frontend is `static/index.html`.

---

## 4. Backend — File-by-File Reference

### `main.py` — FastAPI Application

The main entry point. Handles:
- Serving the frontend (`GET /`)
- Receiving form submissions (`POST /intake`)
- Orchestrating the full AI pipeline

**Key Routes:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves `static/index.html` |
| `POST` | `/intake` | Processes patient intake form |

**`POST /intake` — Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audio` | File (webm) | Optional | Patient voice recording |
| `text_input` | String | Optional | Typed symptom description |
| `documents` | File[] | Optional | Medical documents (PDF/images) |
| `symptom_images` | File[] | Optional | Photos of symptoms |

**`POST /intake` — Response:**

```json
{
  "intake_form": "# Patient Intake Form\n...(Markdown)...",
  "voice_transcription": "Patient said: ...",
  "documents_analyzed": 2,
  "symptom_images_analyzed": 1
}
```

**Processing Pipeline in `main.py`:**
1. Save uploaded audio → transcribe → delete temp file
2. Save uploaded documents → analyze each → delete temp files
3. Save uploaded symptom images → analyze each → delete temp files
4. Combine all text → run CrewAI workflow → return result

---

### `agents.py` — CrewAI Agents

Defines 4 specialized AI agents, each powered by `gemini-2.0-flash-lite` via `langchain-google-genai`.

| Agent | Role | Responsibility |
|-------|------|----------------|
| `intake_agent` | Patient Intake Specialist | Extracts demographics, chief complaint, symptoms |
| `history_agent` | Medical History Analyst | Extracts past conditions, medications, allergies |
| `document_agent` | Medical Document Analyst | Reads and interprets uploaded documents |
| `summary_agent` | Patient Profile Summarizer | Synthesizes all data into final intake form |

**Model Configuration:**
```python
ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

---

### `tasks.py` — CrewAI Tasks

Defines 4 tasks that map to the 4 agents:

| Task | Agent | Input | Output |
|------|-------|-------|--------|
| `extract_basic_info` | intake_agent | voice/text | Demographics + chief complaint JSON |
| `analyze_documents` | document_agent | document analyses | Extracted medical data |
| `extract_medical_history` | history_agent | voice/text + docs | Medical history summary |
| `generate_intake_form` | summary_agent | all 3 above tasks | Final Markdown intake form |

**Final Intake Form Sections (generated by `generate_intake_form`):**
1. Patient Demographics
2. Chief Complaint & Symptoms
3. Symptom Timeline
4. Medical History
5. Current Medications
6. Allergies
7. Family History
8. Lifestyle & Social History
9. Documents Reviewed
10. Flags & Urgent Notes
11. Doctor Briefing Summary

---

### `multimodal_tools.py` — Gemini Multimodal Functions

Uses the `google-genai` SDK directly for multimodal AI calls.

#### `transcribe_audio(audio_file_path)`
- Converts audio to MP3 (via `pydub`) if needed
- Sends audio bytes to Gemini with transcription prompt
- Returns transcribed text string

#### `analyze_document_image(image_path)`
- Supports: JPG, PNG, PDF, GIF, WebP
- Sends document bytes to Gemini
- Extracts: patient details, medications, diagnoses, lab results, doctor notes

#### `analyze_symptom_image(image_path)`
- Supports: JPG, PNG, GIF, WebP
- Sends image bytes to Gemini
- Describes: visible condition, location, size, color/texture, concerning features

#### `wait_for_active_file(file_name)`
- Helper: polls until an uploaded Gemini file is in `ACTIVE` state
- Retries up to 30 times with 1-second delay

---

### `requirements.txt` — Python Dependencies

```
fastapi              # Web framework
uvicorn              # ASGI server
python-multipart     # For file upload parsing
crewai               # Multi-agent AI framework
langchain-google-genai  # LangChain wrapper for Gemini (used by CrewAI)
google-generativeai  # Google AI SDK
pydub                # Audio conversion (webm → mp3)
python-dotenv        # .env file loading
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

---

## 5. Frontend — `index.html`

A Single Page Application (SPA) with 3 screens, built with:
- **Tailwind CSS** (via CDN) — utility-first styling
- **Google Fonts** — Inter + Playfair Display
- **Material Symbols** — icons
- **Marked.js** — Markdown rendering for the result

### Screen Flow

```
[Screen 1: Input Form] → (submit) → [Screen 2: Processing] → (AI done) → [Screen 3: Result]
                                                                              ↓
                                                                        [Start Over]
                                                                              ↓
                                                                    [Screen 1: Input Form]
```

### Screen 1 — Input Form
- **Reason for Visit** dropdown (12 options)
- **Describe in your own words** textarea
- **Severity slider** (1–10, hidden for checkups/follow-ups)
- **Voice Note** — record audio via microphone
- **Upload Documents** — PDF or images
- **Symptom Photos** — shown only for Skin Condition / Injury or Wound
- **Continue to Review** button → triggers `submitIntake()`

### Screen 2 — Processing
- Animated pulse rings with brain/neurology icon
- 4 animated step indicators showing AI progress
- Steps animate in sequentially with checkmarks

### Screen 3 — Result
- Displays generated intake form as rendered Markdown
- Shows generation date
- **Download as PDF** button (browser print dialog)
- **Start Over** button (resets to Screen 1)

### Key JavaScript Functions

| Function | Description |
|----------|-------------|
| `showScreen(id)` | Switches between screens with fade animation |
| `submitIntake()` | Validates form, builds FormData, calls `POST /intake` |
| `startRecording()` | Starts microphone recording via MediaRecorder API |
| `stopRecording()` | Stops recording, creates audio blob |
| `clearRecording()` | Removes recorded audio |
| `handleDocuments(e)` | Handles document file selection |
| `handleSymptomImages(e)` | Handles symptom image selection |
| `handleSymptomChange()` | Shows/hides severity + photo sections based on symptom type |
| `animateSteps()` | Animates processing step indicators |
| `resetAll()` | Clears all data and returns to Screen 1 |
| `showError(msg)` | Shows error banner on Screen 1 |

---

## 6. AI Workflow (CrewAI Agents)

The CrewAI workflow runs sequentially when `POST /intake` is called:

```
Patient Input (text + audio + docs + images)
        │
        ▼
┌─────────────────────┐
│   intake_agent      │  Task 1: Extract basic info
│   (T1)              │  → Name, age, chief complaint, symptoms, severity
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   document_agent    │  Task 2: Analyze documents
│   (T2)              │  → Medications, lab results, diagnoses
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   history_agent     │  Task 3: Extract medical history
│   (T3)              │  → Past conditions, allergies, family history
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   summary_agent     │  Task 4: Generate final intake form
│   (T4)              │  → Complete Markdown document (11 sections)
└─────────────────────┘
        │
        ▼
   Markdown intake form returned to frontend
```

---

## 7. API Reference

### `GET /`
Returns the frontend HTML page.

**Response:** `text/html` — `static/index.html`

---

### `POST /intake`
Processes patient intake data and returns AI-generated form.

**Request:** `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `audio` | File | Voice recording (webm format from browser) |
| `text_input` | String | Combined symptom text (reason + severity + description) |
| `documents` | File[] | Medical documents (PDF, JPG, PNG) |
| `symptom_images` | File[] | Symptom photos (JPG, PNG) |

**Success Response (200):**
```json
{
  "intake_form": "# Patient Intake Form\n## 1. PATIENT DEMOGRAPHICS\n...",
  "voice_transcription": "Patient reported headache for 3 days...",
  "documents_analyzed": 1,
  "symptom_images_analyzed": 0
}
```

**Error Response (500):**
```json
{
  "error": "Error message here"
}
```

**Common Errors:**
- `429 RESOURCE_EXHAUSTED` — Gemini API quota exceeded
- `404 NOT_FOUND` — Model name not available for API version

---

## 8. Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip
- Google AI Studio API key ([aistudio.google.com](https://aistudio.google.com))
- FFmpeg (required by pydub for audio conversion)

### Step 1: Install FFmpeg
FFmpeg is required for audio conversion (webm → mp3).

**Windows:**
```bash
# Download from https://ffmpeg.org/download.html
# Or via winget:
winget install ffmpeg
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### Step 4: Run the Server
```bash
python main.py
```

### Step 5: Open the App
Navigate to: [http://localhost:8080](http://localhost:8080)

---

## 9. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | Google Gemini API key from AI Studio |

**`.env` file format:**
```
GOOGLE_API_KEY=AIzaSy...your_key_here
```

---

## 10. Running the Application

```bash
# Start the server
python main.py

# Server starts at:
# INFO: Uvicorn running on http://0.0.0.0:8080
```

**To stop the server:** Press `Ctrl + C` in the terminal.

**To restart after code changes:**
```bash
# Stop with Ctrl+C, then:
python main.py
```

---

## 11. Known Issues & Troubleshooting

### ❌ `429 RESOURCE_EXHAUSTED` — Quota Exceeded
**Cause:** Free tier Gemini API quota has been used up.

**Solutions:**
1. Wait until the next day (quotas reset daily)
2. Get a new API key from a different Google account
3. Enable billing on your Google Cloud project

### ❌ `404 NOT_FOUND` — Model Not Available
**Cause:** The specified model name is not available for the API version being used.

**Solution:** Use `gemini-2.0-flash-lite` (currently set in both `agents.py` and `multimodal_tools.py`).

### ❌ `ERR_CONNECTION_REFUSED` — Server Not Running
**Cause:** The FastAPI server is not running.

**Solution:**
```bash
python main.py
```

### ❌ Audio transcription fails
**Cause:** FFmpeg not installed (required by pydub).

**Solution:** Install FFmpeg and ensure it's in your system PATH.

### ❌ Microphone not working in browser
**Cause:** Browser requires HTTPS for microphone access (except on localhost).

**Solution:** Use `http://localhost:8080` (not the IP address).

---

## 12. Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| FastAPI | Latest | Web framework |
| Uvicorn | Latest | ASGI server |
| CrewAI | Latest | Multi-agent AI orchestration |
| LangChain Google GenAI | Latest | LLM interface for CrewAI agents |
| Google GenAI SDK | Latest | Direct Gemini API calls (multimodal) |
| Pydub | Latest | Audio format conversion |
| Python-dotenv | Latest | Environment variable management |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| Tailwind CSS (CDN) | Styling |
| Vanilla JavaScript | Logic & API calls |
| Google Fonts (Inter, Playfair Display) | Typography |
| Material Symbols | Icons |
| Marked.js | Markdown rendering |
| MediaRecorder API | Voice recording |

### AI Models
| Model | SDK | Used For |
|-------|-----|---------|
| `gemini-2.0-flash-lite` | google-genai | Audio transcription, document analysis, image analysis |
| `gemini-2.0-flash-lite` | langchain-google-genai | CrewAI agent reasoning |

---

## 📌 Quick Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key in .env
echo "GOOGLE_API_KEY=your_key" > .env

# Run the app
python main.py

# Open in browser
# http://localhost:8080
```

---

*Documentation generated for IntakeAI v1.0 — February 2026*
