from app.exceptions.common import AppException


class ArticleNotFound(AppException):

    def __init__(self):

        super().__init__(

            message="Article not found.",

            status_code=404

        )


class DuplicateArticle(AppException):

    def __init__(self):

        super().__init__(

            message="Article already exists.",

            status_code=409

        )