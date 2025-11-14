from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import json
from app.schemas.chat import ChatResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_service import query_llm, stream_llm_response
from app.core.cache import generate_cache_key, get_cache, set_cache
from app.api.deps import get_auth_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(
    file: UploadFile = File(...),
    question: str = Form(...),
    current_user: str = Depends(get_auth_user)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_content = await file.read()
    if not file_content:
        raise HTTPException(status_code=400, detail="Empty file")

    cache_key = generate_cache_key(file_content, question)
    cached = get_cache(cache_key)
    if cached:
        return ChatResponse(answer=cached, cached=True)

    pdf_text = extract_text_from_pdf(file_content)
    answer = await query_llm(pdf_text, question)
    set_cache(cache_key, answer)
    return ChatResponse(answer=answer, cached=False)

@router.post("/stream")
async def chat_stream(
    file: UploadFile = File(...),
    question: str = Form(...),
    current_user: str = Depends(get_auth_user)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_content = await file.read()
    if not file_content:
        raise HTTPException(status_code=400, detail="Empty file")

    cache_key = generate_cache_key(file_content, question)
    cached = get_cache(cache_key)
    if cached:
        async def cached_stream():
            yield f"data: {json.dumps({'answer': cached, 'cached': True})}\n\n"
        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    pdf_text = extract_text_from_pdf(file_content)
    return StreamingResponse(
        stream_llm_response(pdf_text, question),
        media_type="text/event-stream"
    )