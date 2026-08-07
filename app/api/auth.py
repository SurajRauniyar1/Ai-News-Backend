from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.user import UserRegister
from app.schemas.user import UserResponse

from app.schemas.token import Token

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    return AuthService.register(

        db=db,

        username=user.username,

        email=user.email,

        password=user.password

    )


@router.post(
    "/login",
    response_model=Token
)
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    return AuthService.login(

        db=db,

        email=form_data.username,

        password=form_data.password

    )