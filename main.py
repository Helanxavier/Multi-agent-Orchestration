import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from crewai import Crew
from agents import PatientIntakeAgents
from tasks import PatientIntakeTasks
from multimodal_tools import transcribe_audio, analyze_document_image, analyze_symptom_image
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Patient Intake Assistant API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"CRITICAL ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )


@app.get("/")
async def root():
    return FileResponse('static/index.html')


@app.post("/intake")
async def process_intake(
    audio: Optional[UploadFile] = File(None),
    text_input: Optional[str] = Form(None),
    documents: Optional[List[UploadFile]] = File(None),
    symptom_images: Optional[List[UploadFile]] = File(None),
):
    # Step 1: Process voice input
    voice_text = "No voice input provided."
    if audio:
        audio_path = os.path.join(TEMP_DIR, audio.filename)
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        print(f"Transcribing audio: {audio.filename}")
        voice_text = transcribe_audio(audio_path)
        os.remove(audio_path)
        print(f"Transcription complete: {voice_text[:100]}...")

    # Combine voice and text input
    if text_input:
        voice_text = f"{voice_text}\n\nAdditional text input: {text_input}"

    # Step 2: Process medical documents
    document_analyses = []
    if documents:
        for idx, doc in enumerate(documents):
            if doc.filename:
                doc_path = os.path.join(TEMP_DIR, f"doc_{idx}_{doc.filename}")
                with open(doc_path, "wb") as f:
                    shutil.copyfileobj(doc.file, f)
                print(f"Analyzing document: {doc.filename}")
                analysis = analyze_document_image(doc_path)
                document_analyses.append(f"Document {idx+1} ({doc.filename}): {analysis}")
                os.remove(doc_path)

    if not document_analyses:
        document_analyses = ["No medical documents provided."]

    # Step 3: Process symptom images
    symptom_analyses = []
    if symptom_images:
        for idx, img in enumerate(symptom_images):
            if img.filename:
                img_path = os.path.join(TEMP_DIR, f"symptom_{idx}_{img.filename}")
                with open(img_path, "wb") as f:
                    shutil.copyfileobj(img.file, f)
                print(f"Analyzing symptom image: {img.filename}")
                analysis = analyze_symptom_image(img_path)
                symptom_analyses.append(f"Symptom Image {idx+1}: {analysis}")
                os.remove(img_path)

    if symptom_analyses:
        voice_text += f"\n\nSymptom Images Analysis: {' | '.join(symptom_analyses)}"

    # Step 4: Run Agentic Workflow
    agents = PatientIntakeAgents()
    tasks = PatientIntakeTasks()

    intake_agent = agents.intake_agent()
    history_agent = agents.history_agent()
    document_agent = agents.document_agent()
    summary_agent = agents.summary_agent()

    t1 = tasks.extract_basic_info(intake_agent, voice_text)
    t2 = tasks.analyze_documents(document_agent, document_analyses)
    t3 = tasks.extract_medical_history(history_agent, voice_text, document_analyses)
    t4 = tasks.generate_intake_form(summary_agent, [t1, t2, t3])

    crew = Crew(
        agents=[intake_agent, document_agent, history_agent, summary_agent],
        tasks=[t1, t2, t3, t4],
        verbose=True
    )

    print("Starting CrewAI workflow...")
    result = crew.kickoff()
    print("Workflow complete!")

    return {
        "intake_form": str(result),
        "voice_transcription": voice_text,
        "documents_analyzed": len(document_analyses),
        "symptom_images_analyzed": len(symptom_analyses)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
