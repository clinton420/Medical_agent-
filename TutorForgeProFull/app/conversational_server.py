# 📄 app/conversational_server.py (with few-shot intent detection)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from groq import Groq
from dotenv import load_dotenv
import uuid
import re

from agents.lesson_agent import generate_lesson
from agents.mcq_agent import generate_mcq, check_mcq_answer
from agents.feedback_agent import analyze_feedback
from tools.translator import translate_text
from tools.web_search import web_search
from tools.summarizer import summarize_text
from utils.logger import log_event

load_dotenv()
client = Groq()

app = FastAPI()

# Session store: session_id -> {history, preferred_language}
SESSIONS: Dict[str, Dict] = {}

class ChatInput(BaseModel):
    session_id: str = None
    text: str

@app.post("/chat")
def chat_with_agent(payload: ChatInput):
    session_id = payload.session_id or str(uuid.uuid4())
    user_input = payload.text.strip()

    session = SESSIONS.get(session_id, {"history": [], "preferred_language": "en"})
    history = session["history"]
    history.append({"role": "user", "content": user_input})
    log_event("User Input", f"Session: {session_id}\nText: {user_input}")

    # Handle persistent language switch
    if "from now on" in user_input.lower() and "in" in user_input.lower():
        match = re.search(r"in (\w+)", user_input.lower())
        if match:
            session["preferred_language"] = match.group(1)
            response = f"Okay, I will respond in {match.group(1).capitalize()} from now on."
            history.append({"role": "agent", "content": response})
            session["history"] = truncate_history(history)
            SESSIONS[session_id] = session
            return {"session_id": session_id, "response": response}

    if "translate to" in user_input.lower():
        response = translate_text(user_input)
        history.append({"role": "agent", "content": response})
        session["history"] = truncate_history(history)
        SESSIONS[session_id] = session
        return {"session_id": session_id, "response": response}

    intent = detect_intent(history, user_input)
    log_event("Intent Detected", f"Intent: {intent}")

    topic = extract_topic(history)
    log_event("Extracted Topic", topic)

    try:
        if intent == "lesson":
            response = generate_lesson(user_input)
            update_topic(history, user_input)
            log_event("Lesson Triggered", response)

        elif intent == "mcq":
            if topic == "general":
                response = "Please ask me a lesson question first so I can prepare an MCQ for you."
            else:
                response = generate_mcq(topic)
                history.append({"role": "agent", "mcq": response})
            log_event("MCQ Triggered", str(response))

        elif intent == "answer":
            last_mcq = extract_last_mcq(history)
            if last_mcq:
                response = check_mcq_answer(last_mcq, user_input)
            else:
                response = "No active quiz question found. Please ask for an MCQ first."
            log_event("Answer Evaluation", response)

        elif intent == "feedback":
            response = analyze_feedback(user_input)
            log_event("Feedback Response", response)

        elif intent == "summarize":
            response = summarize_text(user_input)
            log_event("Summarizer Tool", response)

        elif intent == "translate":
            response = translate_text(user_input)
            log_event("Translator Tool", response)

        elif intent == "web_search":
            response = web_search(user_input)
            log_event("Web Search Tool", response)

        else:
            response = generate_lesson(user_input)
            update_topic(history, user_input)
            log_event("Fallback to Lesson", response)

    except Exception as e:
        response = "An internal error occurred."
        log_event("Error", str(e))

    # Auto-translate based on preferred language
    if session["preferred_language"] != "en":
        response = translate_text(f"Translate to {session['preferred_language']}: {response}")
        log_event("Auto Translation", session["preferred_language"])

    history.append({"role": "agent", "content": response})
    session["history"] = truncate_history(history)
    SESSIONS[session_id] = session

    return {"session_id": session_id, "response": response}


def detect_intent(history: List[Dict], user_input: str) -> str:
    full_context = "\n".join([f"{msg['role']}: {msg.get('content', msg.get('mcq', ''))}" for msg in history[-6:]])
    prompt = f"""
You're an intent classification assistant. Your job is to look at the user's latest message and decide the correct intent.

Valid intents:
- lesson
- mcq
- answer
- feedback
- translate
- summarize
- web_search
- other

Here are some examples:
"Can you explain the heart?" → lesson
"How does the brain function?" → lesson
"Teach me about digestion" → lesson
"Give me a quiz" → mcq
"Ask me a question about the lungs" → mcq
"The answer is C" → answer
"My answer is B" → answer
"That was too fast" → feedback
"I didn't understand that" → feedback
"Translate this to Spanish" → translate
"Can you summarize that?" → summarize
"Search the web for kidney disease" → web_search
"Google about neuron function" → web_search
"Hi, how are you?" → other

Conversation history:
{full_context}

User's latest message:
"{user_input}"

Your job is to reply with only one word: lesson, mcq, answer, feedback, translate, summarize, web_search, or other.
"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompt}]
        )
        result = completion.choices[0].message.content.strip().lower()
        log_event("Groq Intent Output", result)
        if result in ["lesson", "mcq", "answer", "feedback", "translate", "summarize", "web_search"]:
            return result
        else:
            return "lesson"
    except Exception as e:
        log_event("Intent Detection Error", str(e))
        return "lesson"


def extract_last_mcq(history):
    for msg in reversed(history):
        if "mcq" in msg:
            return msg["mcq"]
    return None


def extract_topic(history):
    for msg in reversed(history):
        if msg.get("role") == "meta" and "topic" in msg:
            return msg["topic"]
    return "general"


def update_topic(history, topic):
    keyword = topic.strip().split()[-1].lower()
    history.append({"role": "meta", "topic": keyword})


def truncate_history(history):
    return history[-10:]

