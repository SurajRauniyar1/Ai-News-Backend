from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import get_current_user

from app.schemas.user import (
    UserUpdate,
    UserResponse
)

from app.services.auth_service import AuthService

from app.models.user import User


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def profile(
    current_user: User = Depends(get_current_user)
):

    return current_user


@router.put(
    "/",
    response_model=UserResponse
)
def update(

    user: UserUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return AuthService.update_profile(

        db=db,

        current_user=current_user,

        username=user.username,

        avatar=user.avatar,

        bio=user.bio

    )


@router.delete("/")
def delete(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return AuthService.delete_account(

        db=db,

        current_user=current_user

    )