from crewai import Agent
from crewai_tools import ScrapeWebsiteTool

def create_scraper_agent():
    return Agent(
        role="Job Scraper",
        goal="Scrape the latest AI job listings from ai-jobs.net",
        backstory="Expert in web data extraction",
        tools=[ScrapeWebsiteTool()],
        allow_delegation=False
    )
