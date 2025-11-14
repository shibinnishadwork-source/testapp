from pydantic import BaseModel

class ChatResponse(BaseModel):
    answer: str
    cached: bool = False