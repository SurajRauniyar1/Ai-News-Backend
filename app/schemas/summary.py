from pydantic import BaseModel


class SummaryRequest(BaseModel):

    article_id: int


class SummaryResponse(BaseModel):

    summary: str

    sentiment: str

    reading_time: int

    tags: list[str]