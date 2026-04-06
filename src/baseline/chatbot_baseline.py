import os
import sys
import time
import json
import ollama
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv

from telemetry.logger import logger

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


# ──────────────────────────────────────────────
# Ollama Chatbot (local models)
# ──────────────────────────────────────────────
class OllamaChatbot:
    """Chatbot using a local Ollama server (Llama, Phi, Mistral, Gemma, etc.)."""

    SYSTEM_PROMPT = (
        "You are a helpful assistant. Answer the user's questions directly "
        "and concisely. If you don't know something, say so honestly."
    )

    def __init__(
        self,
        model_name: str = "gemma3:1b",
        temperature: float = 0.5,
        top_p: float = 0.7,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.provider = "ollama"
        self.conversation_history: List[Dict[str, str]] = []

        logger.log_event("CHATBOT_INIT", {
            "model": self.model_name,
            "provider": self.provider,
            "temperature": self.temperature,
            "top_p": self.top_p,
        })

    def send_message(self, user_input: str) -> Dict[str, Any]:
        self.conversation_history.append({"role": "user", "content": user_input})

        start_time = time.time()

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.conversation_history,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                }
            )
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                return {
                    "content": f"❌ Model '{self.model_name}' not found. Pull it first: ollama pull {self.model_name}",
                    "usage": {},
                    "latency_ms": 0,
                    "provider": self.provider,
                }
            else:
                return {
                    "content": f"❌ Error: {error_msg}",
                    "usage": {},
                    "latency_ms": 0,
                    "provider": self.provider,
                }

        latency_ms = int((time.time() - start_time) * 1000)

        content = response["message"]["content"]
        usage = {
            "prompt_tokens": response.get("prompt_eval_count", 0),
            "completion_tokens": response.get("eval_count", 0),
            "total_tokens": response.get("prompt_eval_count", 0) + response.get("eval_count", 0),
        }

        self.conversation_history.append({"role": "assistant", "content": content})

        logger.log_event("CHATBOT_RESPONSE", {
            "model": self.model_name,
            "provider": self.provider,
            "user_input": user_input,
            "response": content[:200],
            "usage": usage,
            "latency_ms": latency_ms,
        })

        return {
            "content": content,
            "usage": usage,
            "latency_ms": latency_ms,
            "provider": self.provider,
        }

    def reset(self):
        self.conversation_history = []
        logger.log_event("CHATBOT_RESET", {"model": self.model_name})


# ──────────────────────────────────────────────
# Setup wizard & Interactive CLI
# ──────────────────────────────────────────────
def get_float(prompt: str, default: float, min_val: float = 0.0, max_val: float = 2.0) -> float:
    """Prompt the user for a float within a range."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid number. Try again.")


def configure_parameters():
    """Let the user set temperature and top_p."""
    print("\n⚙️   Configure generation parameters:")
    temperature = get_float("  Temperature (0.0 – 2.0)", default=0.5, max_val=2.0)
    top_p = get_float("  Top-P      (0.0 – 1.0)", default=0.7, max_val=1.0)
    return temperature, top_p


def main():
    print("=" * 60)
    print("  💬  Ollama Chatbot Baseline  (no tools / no reasoning loop)")
    print("=" * 60)

    # Use defaults directly - no prompts
    model_name = DEFAULT_MODEL
    temperature = 0.5
    top_p = 0.7

    # Create chatbot
    print(f"\n🚀  Starting chatbot  →  model={model_name}  "
          f"temp={temperature}  top_p={top_p}")
    print("-" * 60)

    chatbot = OllamaChatbot(
        model_name=model_name, 
        temperature=temperature, 
        top_p=top_p
    )

    # Chat loop
    print("Type your message and press Enter. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = chatbot.send_message(user_input)

        print(f"\nAssistant: {result['content']}")
        usage = result.get("usage", {})
        if usage:
            print(
                f"  ⏱  {result['latency_ms']}ms  |  "
                f"🪙 {usage.get('total_tokens', '?')} tokens\n"
            )
        else:
            print()


if __name__ == "__main__":
    main()
