import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database import engine
from app.models.user import Base, User
from app.api.v1 import auth, chat
from app.core.security import token_blacklist
from app.database import get_db

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDF Chatbot API",
    description="Secure FastAPI app for PDF-based Q&A with LLM",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

# Simple logout (access token from header)
security = HTTPBearer()

@app.post("/api/v1/auth/logout")
def logout(credentials=Depends(security)):
    token = credentials.credentials
    token_blacklist.add(token)
    return {"message": "Successfully logged out"}

@app.get("/")
def root():
    return {"message": "PDF Chatbot API", "docs": "/docs"}