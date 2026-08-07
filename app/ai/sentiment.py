from app.ai.groq_client import GroqClient

from app.ai.prompt_builder import SENTIMENT_PROMPT


def analyze_sentiment(content: str):

    if not content:

        return "Unknown"

    return GroqClient.generate(

        system_prompt=SENTIMENT_PROMPT,

        user_prompt=content,

        temperature=0,

        max_tokens=20,

    )