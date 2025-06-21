from crewai import Crew
from agents.scraper_agent import create_scraper_agent
from agents.filter_agent import create_filter_agent
from agents.messenger_agent import create_messenger_agent

def create_job_crew():
    scraper = create_scraper_agent()
    filterer = create_filter_agent()
    messenger = create_messenger_agent()

    return Crew(
        agents=[scraper, filterer, messenger],
        process="sequential",  
        verbose=True
    )
