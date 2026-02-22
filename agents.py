from dotenv import load_dotenv
import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class PatientIntakeAgents:
    def _get_llm(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def intake_agent(self):
        return Agent(
            role="Patient Intake Specialist",
            goal="Conduct a warm, professional patient intake interview. Extract personal details, chief complaint, symptoms, duration, and severity.",
            backstory="You are an experienced medical receptionist and intake specialist. You ask clear, empathetic questions to gather complete patient information before their doctor's visit.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def history_agent(self):
        return Agent(
            role="Medical History Analyst",
            goal="Extract and organize past medical history, current medications, allergies, family history, and lifestyle factors from patient-provided documents and speech.",
            backstory="You are a clinical data specialist who excels at extracting structured medical history from unstructured patient inputs including documents, images, and spoken descriptions.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def document_agent(self):
        return Agent(
            role="Medical Document Analyst",
            goal="Analyze uploaded medical documents, prescriptions, lab reports, and images to extract relevant patient information.",
            backstory="You are an expert in reading and interpreting medical documents. You can identify medications, diagnoses, test results, and clinical notes from any medical document.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def summary_agent(self):
        return Agent(
            role="Patient Profile Summarizer",
            goal="Synthesize all gathered patient information into a clean, structured intake form ready for the doctor.",
            backstory="You are a clinical documentation expert who creates precise, well-organized patient profiles that help doctors quickly understand a patient's situation before the consultation.",
            llm=self._get_llm(),
            verbose=True,
            allow_delegation=False
        )
