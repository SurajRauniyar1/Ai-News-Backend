from app.ai.groq_client import GroqClient

from app.ai.prompt_builder import SUMMARY_PROMPT


def generate_summary(content: str):

    if not content:

        return ""

    return GroqClient.generate(

        system_prompt=SUMMARY_PROMPT,

        user_prompt=content,

        temperature=0.2,

        max_tokens=250,

    )