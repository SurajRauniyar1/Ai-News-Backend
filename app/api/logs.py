from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.api_log_repository import APILogRepository


router = APIRouter(

    prefix="/logs",

    tags=["Logs"]

)


@router.get("/")
def logs(

    db: Session = Depends(get_db)

):

    return APILogRepository.get_logs(

        db

    )