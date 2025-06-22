from llm.ollama_llm import Ollama

def create_local_llm():
    return Ollama(model_name="mistral")
