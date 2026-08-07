from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import get_current_user

from app.services.bookmark_service import BookmarkService


router = APIRouter(

    prefix="/bookmark",

    tags=["Bookmarks"]

)


@router.post("/{article_id}")
def add(

    article_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return BookmarkService.add_bookmark(

        db,

        current_user.id,

        article_id

    )


@router.delete("/{article_id}")
def remove(

    article_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return BookmarkService.remove_bookmark(

        db,

        current_user.id,

        article_id

    )


@router.get("/")
def list_bookmarks(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return BookmarkService.get_bookmarks(

        db,

        current_user.id

    )