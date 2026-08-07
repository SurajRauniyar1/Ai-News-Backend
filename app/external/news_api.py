import httpx

from app.core.config import settings


BASE_URL = "https://newsapi.org/v2"


async def get_top_headlines(
    category: str = "general",
    country: str = "us",
    page: int = 1,
    page_size: int = 20,
):

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.get(

            f"{BASE_URL}/top-headlines",

            params={

                "country": country,

                "category": category,

                "page": page,

                "pageSize": page_size,

                "apiKey": settings.NEWS_API_KEY,

            },

        )

        response.raise_for_status()

        return response.json()


async def search_news(
    query: str,
    page: int = 1,
):

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.get(

            f"{BASE_URL}/everything",

            params={

                "q": query,

                "page": page,

                "pageSize": 20,

                "sortBy": "publishedAt",

                "apiKey": settings.NEWS_API_KEY,

            },

        )

        response.raise_for_status()

        return response.json()