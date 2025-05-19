import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env (for GROQ_API_KEY)
load_dotenv()
client = Groq()

def analyze_feedback(text: str) -> str:
    """
    Uses Groq LLaMA 3.3 to analyze student feedback in a thoughtful and empathetic way.
    Saves both the original input and AI's interpretation to a feedback log file.
    """
    prompt = (
        f"Analyze the following student feedback and provide a helpful interpretation. "
        f"Be detailed and empathetic:\n\n"
        f"Feedback: \"{text}\""
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    analysis = completion.choices[0].message.content.strip()
    save_feedback(text, analysis)
    return analysis

def save_feedback(feedback_text: str, ai_response: str):
    """
    Saves the student feedback and AI analysis to feedback_log.json as a JSON line.
    """
    log_entry = {
        "timestamp": str(datetime.now()),
        "feedback": feedback_text,
        "analysis": ai_response
    }

    with open("feedback_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

