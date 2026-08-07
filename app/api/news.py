from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.news_service import NewsService

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.post("/sync/newsapi/{category}")
async def sync_newsapi(
    category: str,
    db: Session = Depends(get_db)
):

    return await NewsService.sync_newsapi(
        db=db,
        category=category
    )


@router.post("/sync/gnews/{category}")
async def sync_gnews(
    category: str,
    db: Session = Depends(get_db)
):

    return await NewsService.sync_gnews(
        db=db,
        category=category
    )


@router.post("/sync/guardian/{category}")
async def sync_guardian(
    category: str,
    db: Session = Depends(get_db)
):

    return await NewsService.sync_guardian(
        db=db,
        category=category
    )


@router.post("/sync/all/{category}")
async def sync_all(
    category: str,
    db: Session = Depends(get_db)
):

    return await NewsService.sync_all_sources(
        db=db,
        category=category
    )


@router.get("/latest")
def latest(

    page: int = 1,

    page_size: int = 20,

    db: Session = Depends(get_db)

):

    return NewsService.latest(
        db=db,
        page=page,
        page_size=page_size
    )


@router.get("/category/{category}")
def category(

    category: str,

    page: int = 1,

    page_size: int = 20,

    db: Session = Depends(get_db)

):

    return NewsService.category(

        db=db,

        category=category,

        page=page,

        page_size=page_size

    )


@router.get("/search")
def search(

    keyword: str,

    page: int = 1,

    page_size: int = 20,

    db: Session = Depends(get_db)

):

    return NewsService.search(

        db=db,

        keyword=keyword,

        page=page,

        page_size=page_size

    )


@router.get("/trending")
def trending(

    limit: int = 10,

    db: Session = Depends(get_db)

):

    return NewsService.trending(

        db=db,

        limit=limit

    )


@router.get("/{article_id}")
def article(

    article_id: int,

    db: Session = Depends(get_db)

):

    return NewsService.get_article(

        db,

        article_id

    )


@router.put("/{article_id}/refresh")
async def refresh(

    article_id: int,

    db: Session = Depends(get_db)

):

    return await NewsService.refresh_article(

        db,

        article_id

    )


@router.delete("/{article_id}")
def delete(

    article_id: int,

    db: Session = Depends(get_db)

):

    return NewsService.delete_article(

        db,

        article_id

    )


@router.delete("/cleanup/{days}")
def cleanup(

    days: int,

    db: Session = Depends(get_db)

):

    return NewsService.cleanup_old_articles(

        db,

        days

    )


@router.get("/dashboard/stats")
def dashboard(

    db: Session = Depends(get_db)

):

    return NewsService.dashboard_stats(

        db

    )