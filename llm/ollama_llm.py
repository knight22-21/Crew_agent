# llm/ollama_llm.py
from langchain.llms.base import LLM
from typing import Optional, List
import subprocess
from pydantic import Field

class Ollama(LLM):
    model_name: str = Field(default="mistral")  # declare model_name as a Pydantic field

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        cmd = ["ollama", "run", self.model_name, "--prompt", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Ollama CLI error: {result.stderr}")
        return result.stdout.strip()

    @property
    def _llm_type(self) -> str:
        return "ollama"
