from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class APILog(Base):

    __tablename__ = "api_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    endpoint: Mapped[str] = mapped_column(
        String(255)
    )

    method: Mapped[str] = mapped_column(
        String(20)
    )

    status_code: Mapped[int] = mapped_column(
        Integer
    )

    response_time: Mapped[float] = mapped_column(
        Float
    )

    client_ip: Mapped[str] = mapped_column(
        String(100)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )