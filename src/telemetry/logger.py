import logging
import json
import os
from datetime import datetime
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
        }

        # Attach structured data if present
        if hasattr(record, "extra_data"):
            log_record["data"] = record.extra_data

        return json.dumps(log_record)


class IndustryLogger:
    """
    Structured logger with JSON output.
    Safe for reuse (no duplicate handlers).
    """

    def __init__(self, name: str = "AI-Lab-Agent", log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return  # Prevent duplicate logs

        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log"
        )

        formatter = JsonFormatter()

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_event(self, event_type: str, data: Dict[str, Any]):
        self.logger.info(
            event_type,
            extra={"extra_data": data}
        )

    def info(self, msg: str, data: Dict[str, Any] = None):
        self.logger.info(msg, extra={"extra_data": data or {}})

    def error(self, msg: str, data: Dict[str, Any] = None, exc_info=True):
        self.logger.error(msg, extra={"extra_data": data or {}}, exc_info=exc_info)


# Global instance
logger = IndustryLogger()