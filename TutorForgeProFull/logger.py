# utils/logger.py

import datetime
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "../session.log")

def log_event(title: str, content: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {title}:\n{content}\n\n")

