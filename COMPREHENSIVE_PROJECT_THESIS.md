# IntakeAI: A Comprehensive Technical Thesis
## Neural-Orchestrated Multimodal Patient Intake Systems

---

## 📑 Table of Contents
1. **Introduction & Vision**
2. **The Paradigm Shift: AI in Clinical Intake**
3. **Design Philosophy: The Stitch AI Influence**
4. **Integration Protocol: The Stitch MCP Connection**
5. **Architectural Blueprint**
6. **Backend Deep-Dive: FastAPI & Concurrency**
7. **Agentic Layer: The CrewAI Orchestration**
8. **Multimodal Core: Audio, Vision, and OCR**
9. **Frontend Engineering: The SPA Architecture**
10. **Data Security & Privacy (HIPAA Alignment)**
11. **Testing & Verification Methodologies**
12. **Scalability & Future Integration (HL7 FHIR)**
13. **Conclusion: The Future of Autonomous Clinics**

---

## 1. Introduction & Vision
IntakeAI was conceived to solve the "Clinical Bottleneck"—the slow and often error-prone process of manually capturing patient data during intake. By combining high-fidelity UI design with agentic AI, we have created a system that feels human but processes data with surgical precision.

### 1.1 Objective
The primary objective of IntakeAI is to minimize the "clerical burden" on medical staff. By the time a patient walks from the waiting room to the examination room, the provider should already have a structured, prioritized medical brief in their hands.

---

## 2. Design Philosophy: The Stitch AI Influence
The visual identity of IntakeAI is not accidental; it is a meticulously engineered "Trust Interface" generated through **Stitch AI**.

### 2.1 The "Trust Teal" Palette
We utilized `#1a6b59` as our anchor color. In clinical psychology, deep teal is associated with competence, calm, and cleanliness. 

### 2.2 Typography Selection
- **Serif (Playfair Display)**: Used for headers to evoke the authority and tradition of medical institutions.
- **Sans-Serif (Inter)**: Used for data input and body text to ensure maximum readability under varying lighting conditions of a clinic.

---

## 3. Integration Protocol: The Stitch MCP Connection
A unique technical feature of this project is the use of the **Model Context Protocol (MCP)** via the **Stitch Server**. This protocol acted as the digital bridge between the AI agent and the specialized UI generation engine.

### 3.1 What is Stitch MCP?
Stitch MCP is a standardized communication layer that allows the development agent to call external UI generation tools as native functions. This enabled real-time "conversational design," where the user's high-level medical requirements were translated into structured HTML/CSS schemas instantaneously.

### 3.2 Workflow Integration
1. **Connection**: The agent connected to the Stitch MCP server to retrieve project and screen context.
2. **Context Injection**: Medical-specific design tokens (teal palettes, serif typography) were injected into the Stitch context.
3. **Generation**: Stitch generated the 4-state SPA architecture (Landing, Form, Processing, Result) based on these clinical constraints.
4. **Extraction**: The generated assets were pulled through the MCP bridge and integrated directly into the FastAPI `static/` directory.

---

## 4. Architectural Blueprint
The system follows a de-coupled, event-driven architecture.

### 4.1 Structural Stack
| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Foundation** | Python 3.12 | Core logic and system-level operations. |
| **API Layer** | FastAPI | High-performance asynchronous endpoint management. |
| **UI Engine** | Stitch MCP | Protocol-driven interface generation and design systems. |
| **AI Brain** | Google Gemini 2.0 | Multimodal LLM (Audio/Visual/Text). |
| **Orchestration** | CrewAI | Autonomous agent task management. |
| **Presentation** | Vanilla SPA + Stitch | Premium, lightweight browser interface. |

---

## 4. Agentic Layer: The CrewAI Orchestration
Unlike traditional chatbots, IntakeAI uses a "Crew" of specialized agents that peer-review each other's work.

### 4.1 Agent 1: The Intake Specialist (Triage)
- **Primary Goal**: Detect urgency.
- **Logic**: Analyzes voice transcriptions for "Red Flag" symptoms (shortness of breath, sharp chest pain).

### 4.2 Agent 2: The Document Analyst (Data Integrity)
- **Primary Goal**: Cross-reference.
- **Logic**: Compares patient voice claims against uploaded medical reports (e.g., if a patient says they have high BP, the agent looks for Hypertension in the lab reports).

### 4.3 Agent 3: The Medical History Analyst (Context)
- **Primary Goal**: Historical consolidation.
- **Logic**: Builds a chronological timeline of existing conditions based on multi-source data.

### 4.4 Agent 4: The Profile Summarizer (Synthesis)
- **Primary Goal**: Precision.
- **Logic**: The final quality-control agent that formats the output for a doctor's limited reading time (max 45 seconds).

---

## 5. Multimodal Core: Deep Processing

### 5.1 Speech-to-Text (STT) Logic
Using Gemini's native multimodal capabilities, we bypass traditional STT pipelines. The raw `.webm` audio is sent directly to the model, allowing the AI to hear not just the *words*, but the *tone* and *inflection* (e.g., detecting pain in the voice).

### 5.2 Vision Analysis
The system uses computer vision to analyze symptom photos. 
- **Wound Detection**: Estimates injury size and severity.
- **OCR**: Real-time extraction of lab values from scanned PDF or JPG documents.

---

## 6. Implementation Reference: Key Modules

### 6.1 `main.py` Orchestration
The FastAPI entry point handles the concurrent upload of multiple files. We use `BackgroundTasks` (via FastAPI) to ensure the UI feels responsive while the heavy AI processing happens in the back.

### 6.2 `multimodal_tools.py`
This is the bridge to Gemini. It handles:
- **Audio Conversion**: Ensuring compatibility between browser-recorded WebM and model-friendly MP3/WAV.
- **Image Pre-processing**: Scaling images for optimal token usage without losing clinical detail.

---

## 7. Future Scaling: HL7 FHIR Integration
The next evolution of IntakeAI is direct EMR integration. By outputting the summary in **FHIR (Fast Healthcare Interoperability Resources)** format, the data can be injected directly into a hospital's central database (Epic/Cerner) without manual data entry.

---

## 8. Conclusion
IntakeAI demonstrates that the future of medicine isn't just "more data," but "better-organized data." Through the synergy of **Stitch AI design** and **Gemini Orchestration**, we have built a platform that treats the patient's time as just as valuable as the doctor's.

---
*End of Comprehensive Thesis*
