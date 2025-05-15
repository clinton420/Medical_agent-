import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def route_user_input(user_input: str):
    prompt = f"""
You are a tool routing agent. A user said: "{user_input}".

Choose ONLY ONE of these tools: lesson, web_search, summarize, translate, mcq.
Extract the topic. Return only JSON like:
{{"tool": "lesson", "topic": "HUD"}}
"""

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )

    content = chat_completion.choices[0].message.content.strip().split('\n')[0]
    try:
        tool_info = json.loads(content)
        return tool_info["tool"], tool_info["topic"]
    except:
        return None, None
