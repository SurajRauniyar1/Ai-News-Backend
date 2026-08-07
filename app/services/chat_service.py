from sqlalchemy.orm import Session

from app.repositories.chat_repository import ChatRepository
from app.repositories.news_repository import NewsRepository
from app.services.gemini_service import GeminiService


class ChatService:

    @staticmethod
    def send_message(
        db: Session,
        user_id: int,
        message: str,
        conversation_id: int | None = None,
    ):

        # -------------------------
        # Existing Conversation
        # -------------------------

        if conversation_id:

            conversation = ChatRepository.get_conversation(
                db=db,
                conversation_id=conversation_id,
                user_id=user_id,
            )

            if conversation is None:
                return {
                    "message": "Conversation not found."
                }

        # -------------------------
        # New Conversation
        # -------------------------

        else:

            conversation = ChatRepository.create_conversation(
                db=db,
                user_id=user_id,
                title=message[:50],
            )

        # -------------------------
        # Save User Message
        # -------------------------

        ChatRepository.create_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        # -------------------------
        # Search Relevant News
        # -------------------------

        articles = NewsRepository.search_for_chat(
            db=db,
            query=message,
            limit=5,
        )

        # fallback
        if not articles:

            articles = NewsRepository.latest(
                db=db,
                page=1,
                page_size=5,
            )

        context = ""

        for article in articles:

            context += f"""
Title: {article.title}

Category: {article.category}

Summary:
{article.summary}

Content:
{article.content}

----------------------------------------
"""

        # -------------------------
        # Conversation History
        # -------------------------

        history_messages = ChatRepository.get_messages(
            db=db,
            conversation_id=conversation.id,
        )

        history = ""

        for msg in history_messages:

            history += f"{msg.role}: {msg.content}\n"

        # -------------------------
        # Ask Gemini
        # -------------------------

        answer = GeminiService.ask(
            question=message,
            context=context,
            history=history,
        )

        # -------------------------
        # Save AI Response
        # -------------------------

        ChatRepository.create_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )

        # -------------------------
        # Response
        # -------------------------

        return {
            "conversation_id": conversation.id,
            "answer": answer,
        }

    @staticmethod
    def get_conversations(
        db: Session,
        user_id: int,
    ):

        return ChatRepository.get_user_conversations(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int,
        user_id: int,
    ):

        conversation = ChatRepository.get_conversation(
            db=db,
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            return []

        return ChatRepository.get_messages(
            db=db,
            conversation_id=conversation_id,
        )

    @staticmethod
    def delete_conversation(
        db: Session,
        conversation_id: int,
        user_id: int,
    ):

        conversation = ChatRepository.get_conversation(
            db=db,
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation:

            ChatRepository.delete_conversation(
                db=db,
                conversation=conversation,
            )

        return {
            "message": "Conversation deleted."
        }