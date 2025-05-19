def generate_mcq(topic: str) -> dict:
    return {
        "question": f"What is a key point about {topic}?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A"
    }
