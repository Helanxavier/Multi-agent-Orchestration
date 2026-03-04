import os
from crewai import Agent
from dotenv import load_dotenv

load_dotenv()


class PatientIntakeAgents:

    def get_llm(self):
        """Returns the Groq model name. CrewAI will use our global env proxy."""
        # By returning a string, CrewAI 1.9.3 avoids LangChain attribute errors
        # and instead uses its native OpenAI provider, which we've proxied to Groq.
        return "llama-3.3-70b-versatile"

    def intake_agent(self):
        return Agent(
            role='Initial Patient Intake Specialist',
            goal='Extract identity and chief complaint from {voice_text}. Integrate symptom image analysis findings if present.',
            backstory="""You are a clinical intake expert. You effectively isolate the reason for seeking care 
            and any visual evidence (redness, rashes) provided in the data.""",
            llm=self.get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def history_agent(self):
        return Agent(
            role='Medical History Librarian',
            goal='Synthesize a detailed medical history from voice input and analyzed documents.',
            backstory="""You are an expert at connecting dots. You take the patient's spoken history 
            and cross-reference it with any medical documents provided ({document_analysis}) to create a single, clear history.""",
            llm=self.get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def document_agent(self):
        return Agent(
            role='Clinical Document Analyst',
            goal='Deeply analyze medical documents ({document_texts}) and extract lab values, medications, and findings.',
            backstory="""You are a specialist in reading medical reports and lab results. 
            You translate complex medical jargon into structured data point for the intake form.""",
            llm=self.get_llm(),
            verbose=True,
            allow_delegation=False
        )

    def summary_agent(self):
        return Agent(
            role='Patient Intake Coordinator',
            goal='Compile a professional medical brief that contains ONLY verified data, omitting all empty sections and placeholders.',
            backstory="""You are an expert medical editor. Your goal is to produce a high-density clinical report 
            that respects the doctor's time by removing all 'Not provided' or 'None' placeholders.""",
            llm=self.get_llm(),
            verbose=True,
            allow_delegation=False
        )
