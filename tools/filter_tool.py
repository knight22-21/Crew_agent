from crewai_tools import tool
from llm.local_llm import local_llm  # We'll build this in Phase 3

@tool("filter_jobs_tool")
def filter_jobs_tool(job_text: str) -> str:
    """Uses LLM to filter job listings that are remote and NLP-focused"""
    prompt = f"""You're an expert job filterer.
List only jobs from the below input that are:
- Remote
- Related to NLP, AI, or ML

Jobs:
{job_text}
"""
    return local_llm(prompt)
