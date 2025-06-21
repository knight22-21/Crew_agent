from crewai import Agent

def create_messenger_agent():
    return Agent(
        role="Messenger",
        goal="Format the selected jobs in a WhatsApp-friendly summary",
        backstory="Professional communicator",
        tools=[],  # Could add send tool later
        allow_delegation=False
    )
