import requests
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Perform a real web search using DuckDuckGo and return the top result summary."""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url)
        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    return topic["Text"]
        return f"No summary found for: {query}"
    except Exception as e:
        return f"Search failed: {str(e)}"

