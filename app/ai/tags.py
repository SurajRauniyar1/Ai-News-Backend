from app.ai.groq_client import GroqClient

from app.ai.prompt_builder import TAG_PROMPT


def generate_tags(content: str):

    if not content:

        return []

    response = GroqClient.generate(

        system_prompt=TAG_PROMPT,

        user_prompt=content,

        temperature=0,

        max_tokens=50,

    )

    return [

        tag.strip()

        for tag in response.split(",")

        if tag.strip()

    ]