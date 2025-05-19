from fastapi import FastAPI, Request
from app.main import process_input

app = FastAPI()

@app.post("/call-started")
async def call_trigger(request: Request):
    body = await request.json()
    user_input = body.get("text", "What is AI?")
    response = process_input(user_input)
    return {"response": response}
