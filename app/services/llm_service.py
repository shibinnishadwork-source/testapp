import asyncio
import json
from fastapi import HTTPException, status
import httpx
from app.config import settings


async def query_llm(pdf_text: str, question: str) -> str:
    print("in llm")
    
    
    gemini_api_key = getattr(settings, 'gemini_api_key', None) or settings.hf_api_token
    
    if not gemini_api_key:
        raise HTTPException(status_code=500, detail="API key not set")
    
    max_text_length = 10000  
    if len(pdf_text) > max_text_length:
        pdf_text = pdf_text[:max_text_length] + "..."

    prompt = f"""Based on the following document, answer the question concisely.

Document:
{pdf_text}

Question: {question}

Answer:"""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={gemini_api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 500,
                    }
                }
            )
            
            if response.status_code != 200:
                print(f"Gemini API Error: {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"LLM service error: {response.text}"
                )
            
            result = response.json()
            answer = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return answer or "Could not generate a response."
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request to LLM timed out"
        )
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying LLM: {str(e)}"
        )


async def stream_llm_response(pdf_text: str, question: str):
    answer = await query_llm(pdf_text, question)
    for word in answer.split():
        yield f"data: {json.dumps({'token': word})}\n\n"
        await asyncio.sleep(0.01)