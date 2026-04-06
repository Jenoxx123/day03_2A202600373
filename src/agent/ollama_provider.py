import time
import os
import ollama
from typing import Dict, Any, Optional, Generator

class OllamaProvider:
    """
    LLM Provider for local models using Ollama.
    Supports Llama, Phi, Mistral, Gemma, and other models via Ollama.
    """
    def __init__(self, model_name: str = "gemma3:1b", temperature: float = 0.7, top_p: float = 0.9):
        """
        Initialize the Ollama provider.
        Args:
            model_name: Name of the Ollama model (e.g., gemma3:1b, llama3, phi3, mistral).
            temperature: Sampling temperature (0.0 - 2.0)
            top_p: Nucleus sampling parameter (0.0 - 1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.provider = "ollama"

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response from Ollama.
        Args:
            prompt: User prompt
            system_prompt: Optional system instruction
        Returns:
            Dict with content, usage, latency_ms, and provider
        """
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                }
            )
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise FileNotFoundError(f"Model '{self.model_name}' not found. Pull it first: ollama pull {self.model_name}")
            else:
                raise Exception(f"Ollama error: {error_msg}")

        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        content = response["message"]["content"]
        usage = {
            "prompt_tokens": response.get("prompt_eval_count", 0),
            "completion_tokens": response.get("eval_count", 0),
            "total_tokens": response.get("prompt_eval_count", 0) + response.get("eval_count", 0)
        }

        return {
            "content": content,
            "usage": usage,
            "latency_ms": latency_ms,
            "provider": "ollama"
        }

    def stream(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """
        Stream a response from Ollama.
        Args:
            prompt: User prompt
            system_prompt: Optional system instruction
        Yields:
            Tokens as they are generated
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = ollama.chat(
                model=self.model_name,
                messages=messages,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                }
            )
            
            for chunk in stream:
                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    if content:
                        yield content
        except Exception as e:
            yield f"❌ Error: {str(e)}"