from google import genai
from google.genai.errors import ClientError, ServerError

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


class GeminiService:

    @staticmethod
    def ask(
        question: str,
        context: str,
        history: str = "",
    ) -> str:

        prompt = f"""
You are an AI News Assistant.

Rules:
- Answer ONLY using the provided news context.
- Use the conversation history to understand follow-up questions.
- Do NOT make up information.
- If the answer is not found in the context, reply:
  "I couldn't find relevant news for that question."
- Keep answers concise and well formatted.

========================
Conversation History
========================

{history}

========================
News Context
========================

{context}

========================
User Question
========================

{question}
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )

            if response.text:
                return response.text

            return "Gemini returned an empty response."

        except ClientError as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:

                return (
                    "⚠️ Gemini API quota exceeded.\n\n"
                    "Please wait a minute and try again.\n"
                    "If the problem continues, enable billing or create a new API key."
                )

            if "404" in error:

                return (
                    "⚠️ Gemini model not found.\n"
                    "Please check the model name."
                )

            return f"Gemini Client Error:\n{error}"

        except ServerError:

            return (
                "⚠️ Gemini servers are currently busy.\n"
                "Please try again in a few moments."
            )

        except Exception as e:

            return f"Unexpected Error:\n{str(e)}"