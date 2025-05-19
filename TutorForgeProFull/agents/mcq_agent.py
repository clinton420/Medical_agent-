# 📄 agents/mcq_agent.py (topic-aware MCQ generation)

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def generate_mcq(topic: str) -> dict:
    prompt = f"""
You are a tutor generating one multiple-choice question (MCQ) based strictly on the topic: "{topic}".

Return the MCQ in this JSON format:
{{
  "question": "...",
  "options": [
    "A. ...",
    "B. ...",
    "C. ...",
    "D. ..."
  ],
  "answer": "B"
}}

Avoid general knowledge or language questions. Only focus on the topic.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )

    try:
        return eval(response.choices[0].message.content.strip())
    except Exception as e:
        return {
            "question": f"MCQ generation failed: {str(e)}",
            "options": [],
            "answer": "N/A"
        }

def check_mcq_answer(mcq: dict, user_input: str) -> str:
    correct = mcq.get("answer", "").strip().upper()
    user = user_input.strip().upper()
    
    if correct and correct in user:
        return "✅ Correct! Great job."
    elif correct:
        return f"❌ That's not correct. The right answer is {correct}."
    else:
        return "⚠️ Cannot evaluate the answer — MCQ is incomplete."

