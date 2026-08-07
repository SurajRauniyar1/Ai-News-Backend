from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import get_current_user

from app.services.history_service import HistoryService


router = APIRouter(

    prefix="/history",

    tags=["Reading History"]

)


@router.post("/{article_id}")
def add_history(

    article_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return HistoryService.add_history(

        db,

        current_user.id,

        article_id

    )


@router.put("/{article_id}/duration")
def update_duration(

    article_id: int,

    duration: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return HistoryService.update_duration(

        db,

        current_user.id,

        article_id,

        duration

    )


@router.put("/{article_id}/complete")
def complete(

    article_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return HistoryService.complete_article(

        db,

        current_user.id,

        article_id

    )


@router.get("/")
def history(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return HistoryService.get_history(

        db,

        current_user.id

    )