import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

class CrewAIGroq(ChatOpenAI):
    def call(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)

def test_llm():
    try:
        # Set proxy environment variables (Modern OpenAI client uses BASE_URL)
        os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"
        os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
        
        # We don't even need a subclass if the proxy works!
        # Just use a string for the model.
        agent = Agent(
            role="Tester",
            goal="Test LLM",
            backstory="I am a test agent.",
            llm="llama-3.3-70b-versatile",
            verbose=True
        )
        
        task = Task(description="Say hello", expected_output="A greeting", agent=agent)
        crew = Crew(agents=[agent], tasks=[task])
        
        print("Starting crew kickoff...")
        result = crew.kickoff()
        print("Kickoff success!")
        print(result)
    except Exception as e:
        print(f"Caught error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm()
