from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.database import Base


class ReadingHistory(Base):

    __tablename__ = "reading_history"

    __table_args__ = (

        UniqueConstraint(
            "user_id",
            "article_id",
            name="uq_user_history"
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

    duration: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    read_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="history"
    )

    article = relationship(
        "Article",
        back_populates="history"
    )