from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.schemas.chat_schema import ChatRequest
from app.services.chat_service import ChatService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return ChatService.send_message(
        db=db,
        user_id=current_user.id,
        message=request.message,
        conversation_id=request.conversation_id,
    )


@router.get("/")
def conversations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return ChatService.get_conversations(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{conversation_id}")
def messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return ChatService.get_messages(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )


@router.delete("/{conversation_id}")
def delete(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return ChatService.delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
