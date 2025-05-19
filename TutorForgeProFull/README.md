# TutorForge Pro – Full AI Tutor Agent System

This project combines:
- Groq + LLaMA 3.3 for tool reasoning
- Modular agents (lesson, mcq, feedback)
- Tools (summarizer, translator, web search)
- FastAPI for live server (FastRTC trigger-ready)
- Environment-configured API keys

## How to Run

1. Add your GROQ API key to `.env`
2. Install dependencies:
```bash
pip install groq langchain fastapi python-dotenv uvicorn
```
3. Test in terminal:
```bash
python app/main.py
```
4. Run FastAPI server:
```bash
uvicorn app.fastapi_server:app --host 0.0.0.0 --port 8000
```

## Example Input
```json
{
  "text": "Can you explain photosynthesis?"
}
```

## Output
```
[Router] Tool selected: lesson, Topic: photosynthesis
[Final Output]: Lesson on photosynthesis: ...
```
