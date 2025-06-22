# job_crew.py

from crewai import Crew, Task
from llm.local_llm import create_local_llm
from agents.scraper_agent import create_scraper_agent
from agents.filter_agent import create_filter_agent
from agents.messenger_agent import create_messenger_agent

def create_job_crew():
    # Step 1: Load local LLM (Mistral via Ollama)
    llm = create_local_llm()

    # Step 2: Create agents
    scraper = create_scraper_agent(llm)
    filterer = create_filter_agent(llm)
    messenger = create_messenger_agent(llm)

    # Step 3: Define tasks

    scrape_task = Task(
        description="Scrape the latest job listings from ai-jobs.net",
        expected_output="Raw job listings from the website",
        agent=scraper
    )

    filter_task = Task(
        description="From the scraped jobs, select only remote jobs related to AI, NLP, or ML",
        expected_output="A filtered list of relevant job listings",
        agent=filterer
    )

    messaging_task = Task(
        description="Present the filtered jobs in a clear, readable format",
        expected_output="A well-formatted summary of filtered job listings",
        agent=messenger
    )

    # Step 4: Create and return the Crew
    return Crew(
        agents=[scraper, filterer, messenger],
        tasks=[scrape_task, filter_task, messaging_task],
        process="sequential",
        verbose=True
    )
