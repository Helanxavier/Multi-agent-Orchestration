# 🏥 Patient Intake Assistant

A multimodal AI-powered patient intake system using CrewAI agents and Google Gemini.

## Features
- 🎤 Voice input transcription
- 📄 Medical document analysis (prescriptions, lab reports)
- 🖼 Symptom image analysis
- ✍ Text input
- 🤖 4 specialized AI agents
- 📋 Structured intake form output (Markdown)
- 🖨 Print/PDF export

## Agents
1. **Intake Specialist** — Extracts symptoms and chief complaint
2. **Document Analyst** — Reads medical documents and images
3. **Medical History Analyst** — Organizes past history, medications, allergies
4. **Profile Summarizer** — Generates the final structured intake form

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
# Add your GOOGLE_API_KEY to .env
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage
1. Start backend: `python main.py` (runs on port 8000)
2. Start frontend: `npm run dev` (runs on port 5173)
3. Open browser at `http://localhost:5173`
4. Provide voice/text/documents and click "Generate Intake Form"

## API Endpoint
`POST /intake`
- `audio` (file, optional) — Voice recording
- `text_input` (string, optional) — Typed symptoms/history
- `documents` (files, optional) — Medical documents/images
- `symptom_images` (files, optional) — Photos of symptoms
