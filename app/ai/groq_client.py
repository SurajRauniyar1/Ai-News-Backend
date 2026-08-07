from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqClient:

    @staticmethod
    def generate(
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:

        try:

            response = client.chat.completions.create(

                model=DEFAULT_MODEL,

                temperature=temperature,

                max_tokens=max_tokens,

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt,
                    },

                    {
                        "role": "user",
                        "content": user_prompt,
                    },

                ],

            )

            return response.choices[0].message.content.strip()

        except Exception as e:

            raise Exception(
                f"Groq Error: {str(e)}"
            )