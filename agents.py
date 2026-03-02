from dotenv import load_dotenv
import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class PatientIntakeAgents:
    def _get_llm(self):
        # We use gemini-2.0-flash as it was confirmed available
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def intake_agent(self):
        return Agent(
            role="Patient Intake Specialist",
            goal="Conduct the initial patient interview and gather basic information and symptoms.",
            backstory="You are a friendly and efficient medical assistant. Your goal is to make patients feel comfortable while accurately collecting their primary reason for the visit.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def history_agent(self):
        return Agent(
            role="Medical History Researcher",
            goal="Analyze the patient's past medical history, medications, and lifestyle factors.",
            backstory="You are detail-oriented and thorough. You look for patterns in medical history and ensure all relevant past conditions and medications are documented.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def document_agent(self):
        return Agent(
            role="Medical Document Specialist",
            goal="Analyze medical documents and lab results to extract key clinical findings.",
            backstory="You are an expert at interpreting clinical documents, lab reports, and imaging results. You focus on extracting accurate data points that are relevant to the current visit.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def summary_agent(self):
        return Agent(
            role="Patient Profile Summarizer",
            goal="Synthesize all gathered information into a structured, professional patient intake form.",
            backstory="You are skilled at medical transcription and clinical summaries. You take complex information and organize it into a clear, concise format for the physician.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )
