from crewai import Agent
from crewai_tools.tools import ScrapeWebsiteTool

def create_scraper_agent(llm):
    return Agent(
        role="Job Scraper",
        goal="Scrape the latest AI job listings from ai-jobs.net",
        backstory="Expert in web data extraction",
        llm=llm,
        tools=[ScrapeWebsiteTool(website_url="https://ai-jobs.net")],
        allow_delegation=False
    )
