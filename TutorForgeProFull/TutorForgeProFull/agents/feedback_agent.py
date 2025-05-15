def analyze_feedback(text: str) -> str:
    if "confusing" in text.lower():
        return "confused"
    elif "easy" in text.lower():
        return "understood"
    return "neutral"
