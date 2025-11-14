from pydantic import BaseModel
from app.core.security import get_current_user

# Just alias it or use directly — no wrapper needed
get_auth_user = get_current_user
class ChatResponse(BaseModel):
    answer: str
    cached: bool = False