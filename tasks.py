from crewai import Task

class PatientIntakeTasks:

    def extract_basic_info(self, agent, voice_text):
        return Task(
            description=f"""
            Analyze the patient input (voice transcription and any symptom image analysis) and extract:
            - Full name
            - Age and date of birth
            - Gender
            - Chief complaint
            - Symptom description (incorporate visual findings from image analysis if present)
            - Duration and Severity
            - Urgent/emergency flags

            Input Data: {voice_text}

            IMPORTANT: ONLY extract information that is explicitly mentioned. Do NOT use placeholders like 'Not provided'. 
            If a field is missing, simply omit it from your extraction.
            """,
            expected_output="A structured summary of the patient's identity and primary reason for the visit, prioritizing visual symptom data if available.",
            agent=agent
        )

    def extract_medical_history(self, agent, voice_text, document_analysis):
        return Task(
            description=f"""
            Synthesize medical history from:
            Patient Input: {voice_text}
            Document Analysis: {document_analysis}

            Extract ONLY confirmed information regarding:
            - Past conditions
            - Surgeries
            - Medications (Name, dose, frequency)
            - Allergies
            - Family history
            - Lifestyle (Smoking/Alcohol)

            Omit any category where no information is provided. Do NOT use 'None mentioned' or similar placeholders.
            """,
            expected_output="A concise medical history summary containing only confirmed patient data.",
            agent=agent
        )

    def analyze_documents(self, agent, document_texts):
        return Task(
            description=f"""
            Analyze the following extracted text from patient-uploaded medical documents:
            {document_texts}

            Extract:
            - Medication names, dosages, and prescribing doctors
            - Lab results and their reference ranges
            - Previous diagnoses
            - Doctor's notes and recommendations
            - Dates of previous visits
            - Any abnormal findings
            """,
            expected_output="A detailed extraction of all medical information found in the documents.",
            agent=agent
        )

    def generate_intake_form(self, agent, context):
        return Task(
            description="""
            Assemble the final professional medical intake form.
            
            CRITICAL RULES:
            1. ONLY include sections where information was actually provided.
            2. If 'PATIENT DEMOGRAPHICS' only has Age, only show Age. Omit 'Full Name' if missing.
            3. If 'MEDICAL HISTORY' is empty, OMIT the entire section.
            4. Do NOT use placeholders like 'Not provided', 'None', or 'Not mentioned'.
            5. Ensure 'SYMPTOM DESCRIPTION' integrates findings from any uploaded symptom images (e.g., redness, rash).
            6. Use clean Markdown headers.

            The goal is a 'high-signal' report that only contains useful data for the doctor.
            """,
            expected_output="A clean, concise professional medical brief in Markdown that omits empty sections and placeholders.",
            agent=agent,
            context=context
        )
