from sqlalchemy.orm import Session

from app.models.chat import ChatConversation, ChatMessage


class ChatRepository:

    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
        title: str,
    ):

        conversation = ChatConversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int,
        user_id: int,
    ):

        return (
            db.query(ChatConversation)
            .filter(
                ChatConversation.id == conversation_id,
                ChatConversation.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(ChatConversation)
            .filter(
                ChatConversation.user_id == user_id
            )
            .order_by(
                ChatConversation.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def create_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ):

        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int,
    ):

        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.conversation_id == conversation_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def delete_conversation(
        db: Session,
        conversation: ChatConversation,
    ):

        db.delete(conversation)
        db.commit()

    @staticmethod
    def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 10,
):
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
            .all()
    )