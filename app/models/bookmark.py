from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.database import Base


class Bookmark(Base):

    __tablename__ = "bookmarks"

    __table_args__ = (

        UniqueConstraint(
            "user_id",
            "article_id",
            name="uq_user_bookmark"
        ),

    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    article_id: Mapped[int] = mapped_column(
        ForeignKey(
            "articles.id",
            ondelete="CASCADE"
        )
    )

    user = relationship(
        "User",
        back_populates="bookmarks"
    )

    article = relationship(
        "Article",
        back_populates="bookmarks"
    )