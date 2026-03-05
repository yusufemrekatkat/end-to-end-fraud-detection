"""Prediction logging and system metrics.
Logs every prediction for auditing and future retraining.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

class PredictionLogger:
    """Append-only prediction logger using JSON Lines format."""

    def __init__(self, log_dir: Path) -> None:
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / "predictions.jsonl"

    def log_prediction(self, prediction: dict) -> None:
        """Append a prediction record to the log file."""
        record = {
            "logged_at": datetime.now(timezone.utc).isoformat(),
            **prediction,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record) + "\n")