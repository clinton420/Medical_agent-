from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Search for recent data (mock)."""
    return f"Search result summary for: {query}"
