import json
import os
from datetime import datetime

LOG_DIR = os.getenv("LOG_DIR", "monitoring/logs")
LOG_FILE = os.path.join(LOG_DIR, "app.jsonl")


def log_request(inputs: dict, result: dict | None, latency_ms: float, error: str | None) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "inputs": inputs,
        "result": result,
        "latency_ms": round(latency_ms, 2),
        "error": error,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
