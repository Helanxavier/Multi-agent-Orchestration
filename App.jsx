import { useState, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://localhost:8000";

export default function App() {
  const [step, setStep] = useState(1); // 1: input, 2: processing, 3: result
  const [textInput, setTextInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [symptomImages, setSymptomImages] = useState([]);
  const [intakeForm, setIntakeForm] = useState("");
  const [error, setError] = useState("");
  const [processingStatus, setProcessingStatus] = useState("");

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setAudioBlob(blob);
        setAudioURL(URL.createObjectURL(blob));
        stream.getTracks().forEach((t) => t.stop());
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      setError("Microphone access denied. Please allow microphone access.");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const handleSubmit = async () => {
    if (!audioBlob && !textInput && documents.length === 0 && symptomImages.length === 0) {
      setError("Please provide at least one input — voice, text, or documents.");
      return;
    }

    setError("");
    setStep(2);
    setProcessingStatus("Uploading your information...");

    const formData = new FormData();

    if (audioBlob) {
      formData.append("audio", audioBlob, "patient_input.webm");
    }
    if (textInput) {
      formData.append("text_input", textInput);
    }
    documents.forEach((doc) => formData.append("documents", doc));
    symptomImages.forEach((img) => formData.append("symptom_images", img));

    try {
      setProcessingStatus("AI agents are analyzing your information...");
      const res = await axios.post(`${API_URL}/intake`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setIntakeForm(res.data.intake_form);
      setStep(3);
    } catch (err) {
      setError("Failed to process intake. Please ensure the backend is running.");
      setStep(1);
    }
  };

  const reset = () => {
    setStep(1);
    setTextInput("");
    setAudioBlob(null);
    setAudioURL(null);
    setDocuments([]);
    setSymptomImages([]);
    setIntakeForm("");
    setError("");
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⚕</span>
            <span className="logo-text">IntakeAI</span>
          </div>
          <p className="header-subtitle">Patient Intake Assistant</p>
        </div>
      </header>

      <main className="main">
        {/* Step 1: Input */}
        {step === 1 && (
          <div className="card fade-in">
            <div className="card-header">
              <h2>Patient Information Intake</h2>
              <p>Provide your details through voice, text, or uploaded documents</p>
            </div>

            {error && <div className="error-banner">⚠ {error}</div>}

            {/* Voice Recording */}
            <section className="section">
              <label className="section-label">
                <span className="section-icon">🎤</span>
                Voice Input
              </label>
              <p className="section-desc">Describe your symptoms, medical history, or any relevant information</p>
              <div className="voice-controls">
                {!isRecording ? (
                  <button className="btn btn-record" onClick={startRecording}>
                    <span className="btn-icon">●</span> Start Recording
                  </button>
                ) : (
                  <button className="btn btn-stop" onClick={stopRecording}>
                    <span className="pulse-dot"></span> Stop Recording
                  </button>
                )}
                {audioURL && (
                  <div className="audio-preview">
                    <audio controls src={audioURL} />
                    <span className="audio-label">✓ Recording saved</span>
                  </div>
                )}
              </div>
            </section>

            {/* Text Input */}
            <section className="section">
              <label className="section-label">
                <span className="section-icon">✍</span>
                Text Input
              </label>
              <p className="section-desc">Type your symptoms, concerns, or medical history</p>
              <textarea
                className="textarea"
                placeholder="e.g. I've been experiencing chest pain for 3 days, I take metformin 500mg daily, I'm allergic to penicillin..."
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                rows={5}
              />
            </section>

            {/* Document Upload */}
            <section className="section">
              <label className="section-label">
                <span className="section-icon">📄</span>
                Medical Documents
              </label>
              <p className="section-desc">Upload prescriptions, lab reports, or any medical records</p>
              <div
                className="upload-zone"
                onClick={() => document.getElementById("doc-upload").click()}
              >
                <input
                  id="doc-upload"
                  type="file"
                  multiple
                  accept="image/*,.pdf"
                  style={{ display: "none" }}
                  onChange={(e) => setDocuments(Array.from(e.target.files))}
                />
                <span className="upload-icon">📋</span>
                <span>Click to upload documents</span>
                <span className="upload-hint">Images, PDFs accepted</span>
              </div>
              {documents.length > 0 && (
                <div className="file-list">
                  {documents.map((f, i) => (
                    <div className="file-item" key={i}>
                      <span>📄 {f.name}</span>
                      <button onClick={() => setDocuments(documents.filter((_, idx) => idx !== i))}>✕</button>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Symptom Images */}
            <section className="section">
              <label className="section-label">
                <span className="section-icon">🖼</span>
                Symptom Photos
              </label>
              <p className="section-desc">Upload photos of wounds, rashes, or visible symptoms</p>
              <div
                className="upload-zone"
                onClick={() => document.getElementById("img-upload").click()}
              >
                <input
                  id="img-upload"
                  type="file"
                  multiple
                  accept="image/*"
                  style={{ display: "none" }}
                  onChange={(e) => setSymptomImages(Array.from(e.target.files))}
                />
                <span className="upload-icon">🩺</span>
                <span>Click to upload symptom photos</span>
                <span className="upload-hint">JPG, PNG accepted</span>
              </div>
              {symptomImages.length > 0 && (
                <div className="file-list">
                  {symptomImages.map((f, i) => (
                    <div className="file-item" key={i}>
                      <span>🖼 {f.name}</span>
                      <button onClick={() => setSymptomImages(symptomImages.filter((_, idx) => idx !== i))}>✕</button>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <button className="btn btn-submit" onClick={handleSubmit}>
              Generate Intake Form →
            </button>
          </div>
        )}

        {/* Step 2: Processing */}
        {step === 2 && (
          <div className="card processing-card fade-in">
            <div className="processing-animation">
              <div className="pulse-ring"></div>
              <span className="processing-icon">⚕</span>
            </div>
            <h2>Processing Your Information</h2>
            <p className="processing-status">{processingStatus}</p>
            <div className="agent-steps">
              <div className="agent-step active">🎤 Intake Specialist analyzing voice input</div>
              <div className="agent-step active">📄 Document Analyst reviewing records</div>
              <div className="agent-step active">🏥 Medical History Analyst extracting history</div>
              <div className="agent-step active">📋 Profile Summarizer generating intake form</div>
            </div>
          </div>
        )}

        {/* Step 3: Result */}
        {step === 3 && (
          <div className="card result-card fade-in">
            <div className="result-header">
              <div className="result-badge">✓ Intake Complete</div>
              <h2>Patient Intake Form</h2>
              <p>Ready for doctor review</p>
            </div>
            <div className="intake-form">
              <ReactMarkdown>{intakeForm}</ReactMarkdown>
            </div>
            <div className="result-actions">
              <button className="btn btn-print" onClick={() => window.print()}>
                🖨 Print / Save PDF
              </button>
              <button className="btn btn-reset" onClick={reset}>
                ↺ New Intake
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
