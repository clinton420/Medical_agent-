from langchain.tools import tool

@tool
def summarize_text(text: str) -> str:
    """Summarize complex input."""
    return text[:100] + "..."
