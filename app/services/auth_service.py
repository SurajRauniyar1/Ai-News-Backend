from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(
        db: Session,
        username: str,
        email: str,
        password: str
    ):

        if UserRepository.get_by_email(db, email):
            raise HTTPException(
                status_code=409,
                detail="Email already exists."
            )

        if UserRepository.get_by_username(db, username):
            raise HTTPException(
                status_code=409,
                detail="Username already exists."
            )

        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password)
        )

        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials."
            )

        if not verify_password(
            password,
            user.hashed_password
        ):

            raise HTTPException(
                status_code=401,
                detail="Invalid credentials."
            )

        token = create_access_token(

            {
                "sub": user.email,
                "id": user.id
            }

        )

        return {

            "access_token": token,

            "token_type": "bearer"

        }

    @staticmethod
    def update_profile(
        db: Session,
        current_user,
        username,
        avatar,
        bio
    ):

        if username:
            current_user.username = username

        if avatar:
            current_user.avatar = avatar

        if bio:
            current_user.bio = bio

        return UserRepository.update(
            db,
            current_user
        )

    @staticmethod
    def delete_account(
        db: Session,
        current_user
    ):

        UserRepository.delete(
            db,
            current_user
        )

        return {

            "message":"Account deleted successfully"

        }