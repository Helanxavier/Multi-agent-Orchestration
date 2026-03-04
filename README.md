# 🏥 IntakeAI - Advanced Patient Intake Assistant

IntakeAI is a premium, AI-powered patient intake system that leverages **Groq (Llama-3.3-70B)** for medical intelligence, **OpenAI Whisper (Local)** for voice transcription, and **CrewAI** agents for multimodal orchestration. 

It transforms patient voice recordings, medical documents (PDF/DOCX/TXT), and photos into highly structured, clinical-grade medical briefs ready for providers.

## 🚀 Key Improvements
- **Clinical Intelligence**: Powered by **Llama-3.3-70B-Versatile** on Groq for sub-second analysis.
- **Privacy-First Voice**: Transcribes locally using **Whisper**, ensuring patient voice data stays on-device.
- **High-Signal Summary**: Intelligent reporting that omits missing info and prioritizes visual symptom evidence.
- **Premium SPA UI**: Clean, medical-grade aesthetic with professional print/PDF alignment.
- **Restricted Tooling**: Professional medical file handling for PDF, Word, and Text documents.

## 🤖 AI Agents
1. **Intake Specialist**: Extracts immediate symptoms and prioritizes visual findings from Groq Vision analysis.
2. **Document Analyst**: Extracts structured data from PDF and Word documents with high precision.
3. **Medical History Analyst**: Synthesizes history and medication lists without using generic placeholders.
4. **Profile Summarizer**: Produces a clean, concise Markdown report for the doctor.

## 🛠 Setup & Installation

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Running the Application
Start the FastAPI server:
```bash
python main.py
```
Open your browser and navigate to **http://localhost:8080**.

---
*Powered by Groq & Whisper.*
