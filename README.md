# PDF Chatbot API

A secure FastAPI application that answers questions from PDFs using Mistral-7B via Hugging Face.

## Features
- JWT Authentication (`/signup`, `/login`, `/logout`)
- PDF text extraction & LLM Q&A
- Caching (5-minute TTL)
- Streaming responses
- SQLite database (auto-created)
- Docker support

## Setup

### 1. Clone & Install
```bash
git clone <your-repo>
cd pdf-chatbot
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload to run


i can use may be rag system also 