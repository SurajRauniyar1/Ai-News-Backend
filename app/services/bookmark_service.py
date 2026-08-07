from fastapi import HTTPException

from app.models.bookmark import Bookmark

from app.repositories.news_repository import NewsRepository
from app.repositories.bookmark_repository import BookmarkRepository


class BookmarkService:

    @staticmethod
    def add_bookmark(
        db,
        user_id,
        article_id
    ):

        article = NewsRepository.get_by_id(
            db,
            article_id
        )

        if not article:

            raise HTTPException(
                status_code=404,
                detail="Article not found."
            )

        if BookmarkRepository.exists(
            db,
            user_id,
            article_id
        ):

            raise HTTPException(
                status_code=409,
                detail="Already bookmarked."
            )

        bookmark = Bookmark(

            user_id=user_id,

            article_id=article_id

        )

        return BookmarkRepository.create(
            db,
            bookmark
        )

    @staticmethod
    def remove_bookmark(
        db,
        user_id,
        article_id
    ):

        bookmark = BookmarkRepository.exists(

            db,

            user_id,

            article_id

        )

        if not bookmark:

            raise HTTPException(

                status_code=404,

                detail="Bookmark not found."

            )

        BookmarkRepository.delete(

            db,

            bookmark

        )

        return {

            "message":"Bookmark removed."

        }

    @staticmethod
    def get_bookmarks(
        db,
        user_id
    ):

        return BookmarkRepository.get_user_bookmarks(

            db,

            user_id

        )