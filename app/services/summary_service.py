from fastapi import HTTPException

from app.repositories.news_repository import NewsRepository

from app.ai.summary import generate_summary
from app.ai.sentiment import analyze_sentiment
from app.ai.tags import generate_tags
from app.ai.reading_time import calculate_reading_time


class SummaryService:

    @staticmethod
    def summarize_article(
        db,
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

        article.summary = generate_summary(
            article.content
        )

        article.sentiment = analyze_sentiment(
            article.content
        )

        article.ai_tags = ",".join(

            generate_tags(
                article.content
            )

        )

        article.reading_time = calculate_reading_time(
            article.content
        )

        return NewsRepository.update(
            db,
            article
        )