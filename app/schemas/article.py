from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ArticleBase(BaseModel):

    title: str

    description: str | None

    content: str | None

    image: str | None

    url: str

    source: str

    author: str | None

    category: str

    language: str | None

    country: str | None

    published_at: datetime | None


class ArticleResponse(ArticleBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    summary: str | None

    sentiment: str | None

    ai_tags: str | None

    reading_time: int | None