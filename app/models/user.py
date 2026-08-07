from datetime import datetime

from app.database.database import Base
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    avatar: Mapped[str | None] = mapped_column(String(500), nullable=True)

    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    bookmarks: Mapped[list["Bookmark"]] = relationship(
        "Bookmark", back_populates="user", cascade="all, delete-orphan"
    )

    history: Mapped[list["ReadingHistory"]] = relationship(
        "ReadingHistory", back_populates="user", cascade="all, delete-orphan"
    )
