SUMMARY_PROMPT = """
You are an expert news editor.

Summarize the article.

Requirements:

- Keep summary under 120 words.
- Preserve important facts.
- No opinions.
- Easy to read.
"""

TAG_PROMPT = """
Extract 5 important tags.

Rules:

Return ONLY comma separated tags.

Example:

AI,OpenAI,Technology,Startup,GPT
"""

SENTIMENT_PROMPT = """
Classify the article.

Return ONLY one word.

Positive

Negative

Neutral
"""

RECOMMENDATION_PROMPT = """
Recommend similar news topics.

Return only comma separated topics.
"""