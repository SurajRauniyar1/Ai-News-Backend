import httpx

from app.core.config import settings


BASE_URL = "https://gnews.io/api/v4"


async def get_news(
    category: str = "general"
):

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.get(

            f"{BASE_URL}/top-headlines",

            params={

                "topic": category,

                "lang": "en",

                "country": "us",

                "max": 20,

                "apikey": settings.GNEWS_API_KEY,

            },

        )

        response.raise_for_status()

        return response.json()