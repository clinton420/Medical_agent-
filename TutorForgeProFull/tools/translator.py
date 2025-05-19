# 📄 tools/translator.py (real translation with history awareness)

from langchain.tools import tool
import re
import requests

@tool
def translate_text(text: str, history: list = [], default_lang="es") -> str:
    """
    Translates the given text or the last agent response to the specified language using real API (LibreTranslate).
    Format 1: "Translate to Spanish: The heart pumps blood"
    Format 2: "Please translate that to French"
    """
    # Extract language from input
    match = re.search(r"translate.*to (\w+)", text.lower())
    language = match.group(1) if match else default_lang

    # Handle direct input
    if ":" in text:
        _, content = text.split(":", 1)
        content = content.strip()
    else:
        content = None

    # If no direct content, grab last agent message
    if not content and history:
        for msg in reversed(history):
            if msg.get("role") == "agent" and "content" in msg:
                content = msg["content"]
                break

    if not content:
        return "⚠️ Sorry, I couldn't find anything to translate."

    try:
        # Call LibreTranslate (or use your own service)
        response = requests.post(
            "https://libretranslate.com/translate",
            headers={"Content-Type": "application/json"},
            json={
                "q": content,
                "source": "en",
                "target": language[:2],
                "format": "text"
            },
            timeout=10
        )
        if response.ok:
            translated = response.json().get("translatedText", "[Translation failed]")
            return f"[Translated to {language.capitalize()}]: {translated}"
        else:
            return f"❌ Translation API error: {response.text}"

    except Exception as e:
        return f"❌ Translation failed: {str(e)}"

