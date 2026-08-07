from app.ai.groq_client import GroqClient

from app.ai.prompt_builder import RECOMMENDATION_PROMPT


def recommend_topics(content: str):

    if not content:

        return []

    response = GroqClient.generate(

        system_prompt=RECOMMENDATION_PROMPT,

        user_prompt=content,

        temperature=0.3,

        max_tokens=50,

    )

    return [

        topic.strip()

        for topic in response.split(",")

        if topic.strip()

    ]