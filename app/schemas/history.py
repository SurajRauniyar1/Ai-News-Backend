from pydantic import BaseModel
from pydantic import ConfigDict


class HistoryCreate(BaseModel):

    article_id: int


class HistoryUpdate(BaseModel):

    duration: int

    completed: bool


class HistoryResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    article_id: int

    duration: int

    completed: bool