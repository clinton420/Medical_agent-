
# 🧠 TutorForgePro — Conversational AI Tutoring System with LLM Agents

TutorForgePro is an intelligent multi-agent tutoring system built with **FastAPI**, **Groq LLaMA 3.3**, and custom tools. It mimics a human tutor by reasoning, generating lessons, quizzes, evaluating feedback, translating, summarizing, and searching — all from natural conversations.

## 🚀 Features

- 🗣️ **Natural Language Conversations** — Just ask!
- 📚 **LLM-powered Lesson Agent** — Explains any topic
- ❓ **MCQ Agent** — Generates quizzes from past lessons
- ✅ **Answer Checker** — Evaluates MCQ answers
- 💬 **Feedback Agent** — Understands how well users followed
- 🌍 **Real-Time Translation** — Via LibreTranslate
- 🧠 **Conversation Memory** — Tracks context and session history
- 🔍 **Web Search Tool** — Retrieves live data (mock or real)
- 📝 **Summarizer Tool** — Condenses complex content
- 🗂️ **Modular Agents + Tools** — Cleanly structured for scaling

## 📁 Folder Structure

```
TutorForgeProFull/
│
├── app/
│   └── conversational_server.py     # Main FastAPI logic with intent detection and routing
│
├── agents/
│   ├── lesson_agent.py              # LLM lesson generator
│   ├── mcq_agent.py                 # MCQ generator and evaluator
│   └── feedback_agent.py            # Analyzes user understanding
│
├── tools/
│   ├── translator.py                # Real-time translation via LibreTranslate
│   ├── web_search.py                # Web search (mock or real)
│   └── summarizer.py                # Text summarization
│
├── utils/
│   └── logger.py                    # Event logging for debugging
│
├── .env                             # Store your GROQ & LibreTranslate API keys
└── README.md                        # You're reading it!
```

## 🔧 Setup Instructions

### 1. 🐍 Create a Virtual Environment
```bash
python3 -m venv agents
source agents/bin/activate
```

### 2. 📦 Install Requirements
```bash
pip install -r requirements.txt
```

### 3. 🔐 Create a `.env` file
```bash
touch .env
```

Add your keys:

```
GROQ_API_KEY=your-groq-key
LIBRETRANSLATE_API_KEY=your-libretranslate-key
```

(Optional: self-host LibreTranslate to avoid API key)

## ▶️ Run the Server

```bash
uvicorn app.conversational_server:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Postman Test Flow

### 1. Ask a Lesson
```json
POST /chat
{ "text": "Tell me about the lungs" }
```

### 2. Generate an MCQ
```json
{ "session_id": "<returned_id>", "text": "Ask me a quiz" }
```

### 3. Answer It
```json
{ "session_id": "<returned_id>", "text": "The answer is A" }
```

### 4. Give Feedback
```json
{ "session_id": "<returned_id>", "text": "I got confused a bit" }
```

### 5. Translate (automatic or explicit)
```json
{ "session_id": "<returned_id>", "text": "Translate that to Spanish" }
```

## 🌐 Optional: Use Web Search

Update `tools/web_search.py` to call real search APIs (like SerpAPI or DDG).

## 👨‍🔬 Tech Stack

- 🔁 FastAPI for REST server
- 🧠 Groq + LLaMA 3.3
- 🛠️ LangChain tools for plug-and-play logic
- 🌍 LibreTranslate API
- 📜 JSON-based MCQ & feedback formatting
- 💬 In-memory session context

## 📌 Coming Soon

- [ ] LangGraph integration (multi-step reasoning)
- [ ] Voice agent using Whisper + Google TTS
- [ ] Docker + deployment scripts
