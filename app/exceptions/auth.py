from app.exceptions.common import AppException


class InvalidCredentials(AppException):

    def __init__(self):

        super().__init__(

            message="Invalid email or password.",

            status_code=401

        )


class UserAlreadyExists(AppException):

    def __init__(self):

        super().__init__(

            message="User already exists.",

            status_code=409

        )