from datetime import datetime
from app.core.constants import DEFAULT_PAGE_SIZE
from fastapi import HTTPException
from sqlalchemy.orm import Session
import traceback
from app.models.article import Article
from sqlalchemy import func
from app.models.article import Article
from app.repositories.news_repository import NewsRepository

from app.external.news_api import get_top_headlines
from app.external.gnews import get_news
from app.external.guardian import get_guardian_news

from app.external.normalizer import (
    normalize_newsapi,
    normalize_gnews,
    normalize_guardian,
)

from app.external.cleaner import clean_article

from app.ai.summary import generate_summary
from app.ai.sentiment import analyze_sentiment
from app.ai.tags import generate_tags
from app.ai.reading_time import calculate_reading_time


class NewsService:

    @staticmethod
    def _analyze_article(content: str):

        if not content:
            content = ""

        return {
            "summary": generate_summary(content),
            "sentiment": analyze_sentiment(content),
            "tags": generate_tags(content),
            "reading_time": calculate_reading_time(content),
        }

    @staticmethod
    def _build_article(article: dict):

        ai = NewsService._analyze_article(
            article.get("content", "")
        )

        return Article(

            title=article["title"],

            description=article.get("description"),

            content=article.get("content"),

            summary=ai["summary"],

            image=article.get("image"),

            url=article["url"],

            source=article["source"],

            author=article.get("author"),

            category=article["category"],

            language=article.get("language"),

            country=article.get("country"),

            sentiment=ai["sentiment"],

            ai_tags=",".join(ai["tags"]),

            reading_time=ai["reading_time"],

            published_at=article.get("published_at"),

        )

    @staticmethod
    def _process_articles(
        db: Session,
        raw_articles: list,
        normalizer,
        category: str,
    ):

        saved = []

        skipped = 0

        failed = 0

        for raw in raw_articles:

            try:

                article = normalizer(raw)

                article["category"] = category

                article = clean_article(article)

                if not article.get("title"):
                    skipped += 1
                    continue

                if not article.get("url"):
                    skipped += 1
                    continue

                if NewsRepository.exists(
                    db,
                    article["url"]
                ):
                    skipped += 1
                    continue

                db_article = NewsService._build_article(
                    article
                )

                saved.append(db_article)

            except Exception as e:
                failed += 1
                print("=" * 80)
                print("FAILED ARTICLE")
                print(article)
                traceback.print_exc()
                print("=" * 80)
                print(
                    f"Error processing article: {e}"
                )

                failed += 1

        if saved:

            NewsRepository.bulk_create(
                db,
                saved
            )

        return {

            "saved": len(saved),

            "skipped": skipped,

            "failed": failed,

            "total": len(raw_articles)

        }

    @staticmethod
    async def sync_newsapi(
        db: Session,
        category: str
    ):

        response = await get_top_headlines(
            category
        )

        articles = response.get(
            "articles",
            []
        )

        return NewsService._process_articles(
            db=db,
            raw_articles=articles,
            normalizer=normalize_newsapi,
            category=category,
        )

    @staticmethod
    async def sync_gnews(
        db: Session,
        category: str
    ):

        response = await get_news(
            category
        )

        articles = response.get(
            "articles",
            []
        )

        return NewsService._process_articles(
            db=db,
            raw_articles=articles,
            normalizer=normalize_gnews,
            category=category,
        )

    @staticmethod
    async def sync_guardian(
        db: Session,
        category: str
    ):

        response = await get_guardian_news(
            category
        )

        articles = response.get(
            "results",
            []
        )

        return NewsService._process_articles(
            db=db,
            raw_articles=articles,
            normalizer=normalize_guardian,
            category=category,
        )
    @staticmethod
    def latest(
        db: Session,
        page: int = 1,
        page_size: int = 20,
    ):

        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 20

        if page_size > 100:
            page_size = 100

        return NewsRepository.latest(
            db=db,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def category(
        db: Session,
        category: str,
        page: int = 1,
        page_size: int = 20,
    ):

        if page < 1:
            page = 1

        if page_size > 100:
            page_size = 100

        return NewsRepository.category(
            db=db,
            category=category,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def search(
        db: Session,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
    ):

        if not keyword.strip():

            raise HTTPException(
                status_code=400,
                detail="Search keyword cannot be empty."
            )

        return NewsRepository.search(
            db=db,
            keyword=keyword,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def trending(
        db: Session,
        limit: int = 10,
    ):

        if limit < 1:
            limit = 10

        return NewsRepository.trending(
            db=db,
            limit=limit,
        )

    @staticmethod
    def get_article(
        db: Session,
        article_id: int,
    ):

        article = NewsRepository.get_by_id(
            db,
            article_id,
        )

        if not article:

            raise HTTPException(
                status_code=404,
                detail="Article not found."
            )

        return article

    @staticmethod
    def delete_article(
        db: Session,
        article_id: int,
    ):

        article = NewsRepository.get_by_id(
            db,
            article_id,
        )

        if not article:

            raise HTTPException(
                status_code=404,
                detail="Article not found."
            )

        NewsRepository.delete(
            db,
            article,
        )

        return {
            "message": "Article deleted successfully."
        }

    @staticmethod
    async def refresh_article(
        db: Session,
        article_id: int,
    ):

        article = NewsRepository.get_by_id(
            db,
            article_id,
        )

        if not article:

            raise HTTPException(
                status_code=404,
                detail="Article not found."
            )

        ai = NewsService._analyze_article(
            article.content or ""
        )

        article.summary = ai["summary"]

        article.sentiment = ai["sentiment"]

        article.ai_tags = ",".join(
            ai["tags"]
        )

        article.reading_time = ai["reading_time"]

        return NewsRepository.update(
            db,
            article,
        )

    @staticmethod
    async def sync_all_sources(
        db: Session,
        category: str,
    ):

        newsapi = await NewsService.sync_newsapi(
            db,
            category,
        )

        gnews = await NewsService.sync_gnews(
            db,
            category,
        )

        guardian = await NewsService.sync_guardian(
            db,
            category,
        )

        return {

            "category": category,

            "newsapi": newsapi,

            "gnews": gnews,

            "guardian": guardian,

            "total_saved": (
                newsapi["saved"]
                + gnews["saved"]
                + guardian["saved"]
            ),

            "total_skipped": (
                newsapi["skipped"]
                + gnews["skipped"]
                + guardian["skipped"]
            ),

            "total_failed": (
                newsapi["failed"]
                + gnews["failed"]
                + guardian["failed"]
            ),
        }

    @staticmethod
    def cleanup_old_articles(
        db: Session,
        days: int = 30,
    ):

        if days < 1:

            raise HTTPException(
                status_code=400,
                detail="Days must be greater than zero."
            )

        NewsRepository.delete_old(
            db=db,
            days=days,
        )

        return {

            "message": f"Articles older than {days} days removed."

        }


    

    @staticmethod
    def dashboard_stats(
        db: Session,
    ):  

        latest_articles = NewsRepository.latest(
        db=db,
        page=1,
        page_size=12,
    )

        trending_articles = NewsRepository.trending(
        db=db,
        limit=8,
    )

        featured_article = (
        latest_articles[0]
        if latest_articles
        else None
    )

        total_articles = (
        db.query(func.count(Article.id))
        .scalar()
    )

        total_sources = (
        db.query(Article.source)
        .distinct()
        .count()
    )

        total_categories = (
        db.query(Article.category)
        .distinct()
        .count()
    )

        latest_count = len(latest_articles)

        trending_count = len(trending_articles)

        return {

        "featured": featured_article,

        "latest": latest_articles,

        "trending": trending_articles,

        "stats": {

            "total_articles": total_articles,

            "total_sources": total_sources,

            "total_categories": total_categories,

            "latest_articles": latest_count,

            "trending_articles": trending_count,

        },

    }