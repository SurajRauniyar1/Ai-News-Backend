from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.bookmark import Bookmark


class BookmarkRepository:

    @staticmethod
    def create(

        db: Session,

        bookmark: Bookmark

    ):

        db.add(bookmark)

        db.commit()

        db.refresh(bookmark)

        return bookmark

    @staticmethod
    def exists(

        db: Session,

        user_id: int,

        article_id: int

    ):

        return (

            db.query(Bookmark)

            .filter(

                Bookmark.user_id == user_id,

                Bookmark.article_id == article_id

            )

            .first()

        )

    @staticmethod
    def get_user_bookmarks(
    db: Session,
    user_id: int
):

        return (

        db.query(Article)

        .join(
            Bookmark,
            Bookmark.article_id == Article.id
        )

        .filter(
            Bookmark.user_id == user_id
        )

        .all()

    )
    @staticmethod
    def delete(

        db: Session,

        bookmark: Bookmark

    ):

        db.delete(bookmark)

        db.commit()