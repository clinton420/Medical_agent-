from router.router_agent import route_user_input
from agents.lesson_agent import generate_lesson
from agents.mcq_agent import generate_mcq
from agents.feedback_agent import analyze_feedback
from tools.summarizer import summarize_text
from tools.web_search import web_search
from tools.translator import translate_text

def process_input(input_text):
    tool, topic = route_user_input(input_text)
    if not tool:
        return "Sorry, I couldn't understand your request."

    print(f"[Router] Tool selected: {tool}, Topic: {topic}")

    if tool == "lesson":
        return generate_lesson(topic)
    elif tool == "mcq":
        return generate_mcq(topic)
    elif tool == "summarize":
        return summarize_text(topic)
    elif tool == "translate":
        return translate_text(topic)
    elif tool == "web_search":
        return web_search(topic)
    else:
        return "Tool not implemented yet."

if __name__ == "__main__":
    user_input = "Can you tell me about the brain?"
    result = process_input(user_input)
    print("[Final Output]:", result)
