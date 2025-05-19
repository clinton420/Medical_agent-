from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq()

def generate_lesson(topic: str) -> str:
    prompt = f"""
You are an intelligent tutor. Give a simple, clear, and engaging explanation on the topic: "{topic}".
Use analogies if needed and keep it easy to understand for a student.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an educational assistant who explains concepts simply."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content.strip()

