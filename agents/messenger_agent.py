from crewai import Agent

def create_messenger_agent(llm):
    return Agent(
        role="Messenger",
        goal="Write clear and basic programming examples",
        backstory="A helpful AI that generates simple code.",
        llm=llm  # <-- LangChain-compatible LLM
    )
