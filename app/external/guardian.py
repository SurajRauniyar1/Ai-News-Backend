import httpx

from app.core.config import settings


BASE_URL = "https://content.guardianapis.com"


async def get_guardian_news(
    category: str = "news"
):

    async with httpx.AsyncClient(timeout=20) as client:

        response = await client.get(

            f"{BASE_URL}/search",

            params={

                "section": category,

                "show-fields": "headline,trailText,bodyText,thumbnail",

                "api-key": settings.GUARDIAN_API_KEY,

                "page-size": 20,

            },

        )

        response.raise_for_status()

        data = response.json()
        

        return data["response"]