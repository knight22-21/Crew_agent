from transformers import pipeline

# Load FLAN-T5 or T5-small (choose based on RAM/CPU limits)
llm = pipeline("text2text-generation", model="google/flan-t5-base")

def local_llm(prompt: str) -> str:
    """Use FLAN-T5 for job filtering"""
    result = llm(prompt, max_new_tokens=100)[0]['generated_text']
    return result.strip()
