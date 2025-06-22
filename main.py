from crewai import Agent, Task, Process, Crew, LLM
from crewai_tools.tools import ScrapeWebsiteTool  # <--- this is missing in your version

def create_job_crew():
    # Create the LLM object with Ollama config
    llm = LLM(model="ollama/mistral", base_url="http://localhost:11434")

    # ✅ Create the scraper tool
    scraper_tool = ScrapeWebsiteTool(website_url="https://ai-jobs.net")

    # ✅ Attach the tool to the scraper agent
    scraper = Agent(
        role="Job Scraper",
        goal="Scrape the latest AI job listings from ai-jobs.net",
        backstory="Expert in web data extraction",
        tools=[scraper_tool],  # <-- THIS is the fix
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    filterer = Agent(
        role="Job Filterer",
        goal="Select only jobs that are remote and related to NLP or ML",
        backstory="Experienced job analyst with deep NLP knowledge",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    messenger = Agent(
        role="Messenger",
        goal="Write clear and basic programming examples",
        backstory="A helpful AI that generates simple code.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # ✅ Make the task description tell the agent to use the tool
    scrape_task = Task(
        description="Use your tool to scrape the latest job listings from ai-jobs.net",
        expected_output="Raw job listings scraped from the website using the tool",
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

    # Create crew with agents, tasks, and model info
    crew = Crew(
        agents=[scraper, filterer, messenger],
        model="ollama/mistral",
        tasks=[scrape_task, filter_task, messaging_task],
        cache=True,
        verbose=True,
        process=Process.sequential,
        planning=True,
        planning_llm=llm
    )

    return crew

if __name__ == "__main__":
    crew = create_job_crew()
    print("Using model: ollama/mistral")
    result = crew.kickoff()
    print(result)
