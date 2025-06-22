from crewai import Crew
from agents.scraper_agent import create_scraper_agent
from agents.filter_agent import create_filter_agent
from agents.messenger_agent import create_messenger_agent

def create_job_crew():
    scraper = create_scraper_agent()
    filterer = create_filter_agent()
    messenger = create_messenger_agent()
    
    task = Task(
        description="Write a script that prints 'Hello, World!'",
        expected_output="A clear paragraph format"
    )

    return Crew(
        agents=[scraper, filterer, messenger],
        process="sequential",
        tasks=[task],  
        verbose=True
    )
