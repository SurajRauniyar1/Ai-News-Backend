import re


def clean_article(article: dict):

    cleaned = article.copy()

    for key in [

        "title",

        "description",

        "content",

    ]:

        text = cleaned.get(key)

        if text:

            text = re.sub(r"\s+", " ", text)

            text = text.strip()

            cleaned[key] = text

    return cleaned