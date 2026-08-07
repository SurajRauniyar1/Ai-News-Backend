from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


class Article(Base):

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    content: Mapped[str | None] = mapped_column(
        Text
    )

    summary: Mapped[str | None] = mapped_column(
        Text
    )

    image: Mapped[str | None] = mapped_column(
        String(1000)
    )

    url: Mapped[str] = mapped_column(
        String(1200),
        unique=True,
        index=True
    )

    source: Mapped[str] = mapped_column(
        String(255)
    )

    author: Mapped[str | None] = mapped_column(
        String(255)
    )

    category: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    language: Mapped[str | None] = mapped_column(
        String(50)
    )

    country: Mapped[str | None] = mapped_column(
        String(50)
    )

    sentiment: Mapped[str | None] = mapped_column(
        String(50)
    )

    ai_tags: Mapped[str | None] = mapped_column(
        Text
    )

    reading_time: Mapped[int | None] = mapped_column(
        Integer
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    bookmarks = relationship(
        "Bookmark",
        back_populates="article"
    )

    history = relationship(
        "ReadingHistory",
        back_populates="article"
    )