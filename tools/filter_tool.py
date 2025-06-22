from crewai.tools import tool
from llm.local_llm import local_llm  

@tool("filter_jobs_tool")
def filter_jobs_tool(job_text: str) -> str:
    """Filters jobs for remote + AI/NLP/ML relevance using Hugging Face T5"""
    prompt = f"""
Filter the following job listings and return only the ones that are:
- Remote
- Related to AI, NLP, or ML

{job_text}
"""
    return local_llm(prompt)

