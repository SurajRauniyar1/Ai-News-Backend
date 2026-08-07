from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.article import Article


class NewsRepository:

    @staticmethod
    def create(
        db: Session,
        article: Article,
    ):
        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def bulk_create(
        db: Session,
        articles: list[Article],
    ):
        db.add_all(articles)
        db.commit()

    @staticmethod
    def exists(
        db: Session,
        url: str,
    ):
        return (
            db.query(Article)
            .filter(Article.url == url)
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        article_id: int,
    ):
        return (
            db.query(Article)
            .filter(Article.id == article_id)
            .first()
        )

    @staticmethod
    def latest(
        db: Session,
        page: int,
        page_size: int,
    ):
        return (
            db.query(Article)
            .order_by(Article.published_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @staticmethod
    def category(
        db: Session,
        category: str,
        page: int,
        page_size: int,
    ):
        return (
            db.query(Article)
            .filter(Article.category == category)
            .order_by(Article.published_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @staticmethod
    def search(
        db: Session,
        keyword: str,
        page: int,
        page_size: int,
    ):
        return (
            db.query(Article)
            .filter(
                or_(
                    Article.title.ilike(f"%{keyword}%"),
                    Article.description.ilike(f"%{keyword}%"),
                    Article.content.ilike(f"%{keyword}%"),
                )
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @staticmethod
    def search_for_chat(
        db: Session,
        query: str,
        limit: int = 5,
    ):
        return (
            db.query(Article)
            .filter(
                or_(
                    Article.title.ilike(f"%{query}%"),
                    Article.description.ilike(f"%{query}%"),
                    Article.summary.ilike(f"%{query}%"),
                    Article.content.ilike(f"%{query}%"),
                    Article.ai_tags.ilike(f"%{query}%"),
                    Article.category.ilike(f"%{query}%"),
                    Article.author.ilike(f"%{query}%"),
                    Article.source.ilike(f"%{query}%"),
                )
            )
            .order_by(Article.published_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def trending(
        db: Session,
        limit: int = 10,
    ):
        return (
            db.query(Article)
            .order_by(Article.published_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        article: Article,
    ):
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def delete(
        db: Session,
        article: Article,
    ):
        db.delete(article)
        db.commit()

    @staticmethod
    def delete_old(
        db: Session,
        days: int,
    ):
        from datetime import datetime, timedelta

        cutoff = datetime.utcnow() - timedelta(days=days)

        (
            db.query(Article)
            .filter(Article.published_at < cutoff)
            .delete()
        )

        db.commit()