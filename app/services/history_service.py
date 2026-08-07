from app.models.reading_history import ReadingHistory

from app.repositories.news_repository import NewsRepository
from app.repositories.history_repository import HistoryRepository


class HistoryService:

    @staticmethod
    def add_history(
        db,
        user_id,
        article_id
    ):

        article = NewsRepository.get_by_id(
            db,
            article_id
        )

        if not article:

            raise Exception(
                "Article not found."
            )

        history = HistoryRepository.get(

            db,

            user_id,

            article_id

        )

        if history:

            return history

        history = ReadingHistory(

            user_id=user_id,

            article_id=article_id

        )

        return HistoryRepository.create(

            db,

            history

        )

    @staticmethod
    def update_duration(

        db,

        user_id,

        article_id,

        duration

    ):

        history = HistoryRepository.get(

            db,

            user_id,

            article_id

        )

        history.duration = duration

        return HistoryRepository.update(

            db,

            history

        )

    @staticmethod
    def complete_article(

        db,

        user_id,

        article_id

    ):

        history = HistoryRepository.get(

            db,

            user_id,

            article_id

        )

        history.completed = True

        return HistoryRepository.update(

            db,

            history

        )

    @staticmethod
    def get_history(

        db,

        user_id

    ):

        return HistoryRepository.get_history(

            db,

            user_id

        )