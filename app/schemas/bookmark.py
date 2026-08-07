from pydantic import BaseModel
from pydantic import ConfigDict


class BookmarkCreate(BaseModel):

    article_id: int


class BookmarkResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    article_id: int

    user_id: int