from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.reading_history import ReadingHistory


class HistoryRepository:

    @staticmethod
    def create(
        db: Session,
        history: ReadingHistory
    ):
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def get(
        db: Session,
        user_id: int,
        article_id: int
    ):
        return (
            db.query(ReadingHistory)
            .filter(
                ReadingHistory.user_id == user_id,
                ReadingHistory.article_id == article_id
            )
            .first()
        )

    @staticmethod
    def get_history(
        db: Session,
        user_id: int
    ):

        results = (
            db.query(
                ReadingHistory,
                Article
            )
            .join(
                Article,
                Article.id == ReadingHistory.article_id
            )
            .filter(
                ReadingHistory.user_id == user_id
            )
            .order_by(
                ReadingHistory.read_at.desc()
            )
            .all()
        )

        history = []

        for reading_history, article in results:

            history.append({

                "id": reading_history.id,

                "duration": reading_history.duration,

                "completed": reading_history.completed,

                "read_at": reading_history.read_at,

                "article": article

            })

        return history

    @staticmethod
    def update(
        db: Session,
        history: ReadingHistory
    ):
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def delete(
        db: Session,
        history: ReadingHistory
    ):
        db.delete(history)
        db.commit()