from crewai import Task

class PatientIntakeTasks:

    def extract_basic_info(self, agent, voice_text):
        return Task(
            description=f"""
            Analyze the following patient voice/text input and extract:
            - Full name
            - Age and date of birth
            - Gender
            - Contact information (if mentioned)
            - Chief complaint (main reason for visit)
            - Symptom description
            - Duration of symptoms
            - Severity (1-10 scale if possible)
            - Any urgent/emergency flags

            Patient Input: {voice_text}

            If information is missing, note it as 'Not provided'.
            """,
            expected_output="A structured JSON-like summary of the patient's basic information and chief complaint.",
            agent=agent
        )

    def extract_medical_history(self, agent, voice_text, document_analysis):
        return Task(
            description=f"""
            Based on the patient input and document analysis, extract and organize:
            - Past medical conditions/diagnoses
            - Previous surgeries or hospitalizations
            - Current medications (name, dosage, frequency)
            - Known allergies (medications, food, environmental)
            - Family medical history
            - Lifestyle factors (smoking, alcohol, exercise)
            - Vaccination history (if mentioned)

            Patient Input: {voice_text}
            Document Analysis: {document_analysis}
            """,
            expected_output="A comprehensive medical history summary organized by category.",
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
            Using all gathered information, generate a complete, professional patient intake form with these sections:

            1. PATIENT DEMOGRAPHICS
            2. CHIEF COMPLAINT & SYMPTOMS
            3. SYMPTOM TIMELINE
            4. MEDICAL HISTORY
            5. CURRENT MEDICATIONS
            6. ALLERGIES
            7. FAMILY HISTORY
            8. LIFESTYLE & SOCIAL HISTORY
            9. DOCUMENTS REVIEWED
            10. FLAGS & URGENT NOTES
            11. DOCTOR BRIEFING SUMMARY

            Format it cleanly in Markdown. Be precise and clinically appropriate.
            Mark any missing information clearly. Flag any urgent concerns in red (use **⚠️ URGENT:** prefix).
            """,
            expected_output="A complete, structured patient intake form in Markdown format ready for the doctor.",
            agent=agent,
            context=context
        )
