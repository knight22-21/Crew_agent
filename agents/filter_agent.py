from crewai import Agent
from tools.filter_tool import filter_jobs_tool

def create_filter_agent(llm):
    return Agent(
        role="Job Filterer",
        goal="Select only jobs that are remote and related to NLP or ML",
        backstory="Experienced job analyst with deep NLP knowledge",
        tools=[filter_jobs_tool],
        llm=llm,
        allow_delegation=False
    )
