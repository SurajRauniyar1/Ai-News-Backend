from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.summary_service import SummaryService


router = APIRouter(

    prefix="/summary",

    tags=["Summary"]

)


@router.post("/{article_id}")
def summarize(

    article_id: int,

    db: Session = Depends(get_db)

):

    return SummaryService.summarize_article(

        db,

        article_id

    )