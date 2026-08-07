from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.user import User
from app.models.article import Article
from app.models.bookmark import Bookmark
from app.models.reading_history import ReadingHistory
from app.models.chat import ChatConversation, ChatMessage

from app.database.database import Base, engine
from app.api import auth
from app.api import bookmark
from app.api import history
from app.api import logs
from app.api import news
from app.api import summary
from app.api import user
from app.api.chat import router as chat_router
from app.exceptions.common import (
    AppException,
    app_exception_handler,
)

from app.middleware.logging import LoggingMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI News Aggregator",
    version="1.0.0"
)


# -------------------------
# Exception Handlers
# -------------------------

app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# -------------------------
# Middleware
# -------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    LoggingMiddleware
)


# -------------------------
# Routers
# -------------------------

app.include_router(auth.router)

app.include_router(user.router)

app.include_router(news.router)

app.include_router(bookmark.router)

app.include_router(history.router)

app.include_router(summary.router)

app.include_router(logs.router)
app.include_router(chat_router)


# -------------------------
# Root
# -------------------------

@app.get("/")
def root():
    return {
        "message": "AI News Aggregator Running"
    }