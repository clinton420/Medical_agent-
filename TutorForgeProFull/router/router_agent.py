import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load .env file for GROQ_API_KEY
load_dotenv()
client = Groq()

def route_user_input(user_input: str):
    """
    Uses Groq's LLaMA 3.3 to decide which tool to call (lesson, feedback, etc.)
    and extracts the topic or content needed by that tool.
    """

    prompt = f"""
You are a tool routing agent. A user said: "{user_input}"

Choose ONLY ONE of the following tools to handle the request:
- lesson
- web_search
- summarize
- translate
- mcq
- feedback

Decide the best tool based on the user intent. If the user is providing feedback, select "feedback". If they are asking for an explanation, select "lesson", and so on.

Return ONLY a JSON object like:
{{
  "tool": "<tool_name>",
  "topic": "<text_or_topic>"
}}

Examples:
- "Explain the brain" => {{ "tool": "lesson", "topic": "brain" }}
- "That was confusing" => {{ "tool": "feedback", "topic": "That was confusing" }}
- "Give me an MCQ on WW2" => {{ "tool": "mcq", "topic": "WW2" }}
- "Translate hello to French" => {{ "tool": "translate", "topic": "hello" }}
"""

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}]
    )

    response_text = chat_completion.choices[0].message.content.strip()

    # Use regex to extract the first JSON block from the response
    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if json_match:
        try:
            tool_info = json.loads(json_match.group())
            return tool_info["tool"], tool_info["topic"]
        except Exception as e:
            print("[Router Error] Failed to parse valid JSON object.")
            print("Extracted JSON:", json_match.group())
            return None, None
    else:
        print("[Router Error] No JSON object found in model response.")
        print("Raw response:", response_text)
        return None, None

