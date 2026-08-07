from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserUpdate(BaseModel):

    username: str | None = None

    avatar: str | None = None

    bio: str | None = None


class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    avatar: str | None = None

    bio: str | None = None

    last_login: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class UserProfile(BaseModel):

    id: int

    username: str

    email: EmailStr

    avatar: str | None = None

    bio: str | None = None

    last_login: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class ChangePassword(BaseModel):

    old_password: str

    new_password: str