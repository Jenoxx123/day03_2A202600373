import time
from typing import Dict, Any
from src.telemetry.logger import logger


class PerformanceTracker:
    """
    Tracks LLM usage, latency, and failures.
    """

    def __init__(self):
        self.session_metrics = []

    def track_request(
        self,
        provider: str,
        model: str,
        usage: Dict[str, int],
        latency_ms: int,
        success: bool = True,
        error: str = None,
    ):
        metric = {
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "latency_ms": latency_ms,
            "cost_estimate": self._calculate_cost(model, usage),
            "success": success,
            "error": error,
        }

        self.session_metrics.append(metric)
        logger.log_event("LLM_METRIC", metric)

    def track_failure(self, provider: str, model: str, error: str):
        metric = {
            "provider": provider,
            "model": model,
            "success": False,
            "error": error,
        }

        logger.log_event("LLM_ERROR", metric)

    def _calculate_cost(self, model: str, usage: Dict[str, int]) -> float:
        """
        Ollama is local → cost = 0
        (but keep this for future multi-provider support)
        """
        return 0.0


tracker = PerformanceTracker()