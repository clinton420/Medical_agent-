from langchain.tools import tool

@tool
def translate_text(text: str, lang: str = "es") -> str:
    return f"[Translated to {lang}]: {text}"
