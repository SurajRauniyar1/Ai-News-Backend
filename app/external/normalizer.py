from datetime import datetime


def normalize_newsapi(article):

    return {

        "title": article.get("title"),

        "description": article.get("description"),

        "content": article.get("content"),

        "image": article.get("urlToImage"),

        "url": article.get("url"),

        "source": article.get("source", {}).get("name"),

        "author": article.get("author"),

        "language": "en",

        "country": "us",

        "published_at": datetime.fromisoformat(

            article["publishedAt"].replace("Z", "+00:00")

        ) if article.get("publishedAt") else None,

    }


def normalize_gnews(article):

    return {

        "title": article.get("title"),

        "description": article.get("description"),

        "content": article.get("content"),

        "image": article.get("image"),

        "url": article.get("url"),

        "source": article.get("source", {}).get("name"),

        "author": article.get("source", {}).get("name"),

        "language": "en",

        "country": "us",

        "published_at": datetime.fromisoformat(

            article["publishedAt"].replace("Z", "+00:00")

        ) if article.get("publishedAt") else None,

    }


def normalize_guardian(article):

    fields = article.get("fields", {})

    return {

        "title": fields.get("headline") or article.get("webTitle"),

        "description": fields.get("trailText"),

        "content": fields.get("bodyText"),

        "image": fields.get("thumbnail"),

        "url": article.get("webUrl"),

        "source": "The Guardian",

        "author": "The Guardian",

        "language": "en",

        "country": "uk",

        "published_at": datetime.fromisoformat(

            article["webPublicationDate"].replace("Z", "+00:00")

        ) if article.get("webPublicationDate") else None,

    }