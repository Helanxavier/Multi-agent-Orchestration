# 🏥 IntakeAI - Advanced Patient Intake Assistant

IntakeAI is a premium, AI-powered patient intake system that leverages **Stitch AI** for design, **Google Gemini 2.0 Flash Lite** for intelligence, and **CrewAI** agents for multimodal orchestration. 

It transforms patient voice recordings, medical documents, and photos into structured, clinical-grade medical briefs ready for providers.

## 🚀 Features
- **Premium SPA UI**: High-end medical aesthetic with seamless screen transitions.
- **Multimodal Capture**: Supports text, voice recordings, document uploads (PDF/Images), and symptom photos.
- **Agentic Workflow**: 4 specialized AI agents (Intake, History, Documents, and Summary) work together to synthesize data.
- **FastAPI Backend**: Robust Python backend for real-time processing and AI orchestration.
- **PDF Export**: Print-ready results for efficient clinic workflow.

## 🤖 AI Agents
1. **Intake Specialist**: Extracts immediate symptoms and chief complaints.
2. **Document Analyst**: Deep-reads medical documents and visual symptom data.
3. **Medical History Analyst**: Organizes past history, medication lists, and allergies.
4. **Profile Summarizer**: Synthesizes all data into a professional clinical form.

## 🛠 Setup & Installation

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your Google API Key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Running the Application
Start the FastAPI server:
```bash
python main.py
```
Open your browser and navigate to **http://localhost:8080**.

---
*Powered by Stitch AI & Gemini.*
