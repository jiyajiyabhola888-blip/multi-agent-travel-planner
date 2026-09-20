from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ai_chat_service import AIChatService

router = APIRouter(prefix="/chat", tags=["WanderAI Global Assistant"])


class ChatMessageRequest(BaseModel):
    message: str
    destination_context: Optional[str] = None
    trip_context: Optional[Dict[str, Any]] = None


@router.post("/ask")
def chat_with_wander_ai(req: ChatMessageRequest, db: Session = Depends(get_db)):
    """Converses with WanderAI global travel assistant."""
    response = AIChatService.process_chat_message(
        db=db,
        message=req.message,
        destination_context=req.destination_context,
        trip_context=req.trip_context
    )
    return {
        "success": True,
        "assistant_name": "WanderAI",
        "reply": response["reply"],
        "city": response.get("city"),
        "actions": response.get("actions", []),
        "timestamp": "Just now"
    }
