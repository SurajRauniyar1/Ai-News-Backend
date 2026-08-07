import re

from fastapi import HTTPException


class Validator:

    @staticmethod
    def validate_email(email: str):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, email):

            raise HTTPException(

                status_code=400,

                detail="Invalid email address."

            )

    @staticmethod
    def validate_password(password: str):

        if len(password) < 8:

            raise HTTPException(

                status_code=400,

                detail="Password must contain at least 8 characters."

            )

    @staticmethod
    def validate_username(username: str):

        if len(username) < 3:

            raise HTTPException(

                status_code=400,

                detail="Username must contain at least 3 characters."

            )

    @staticmethod
    def validate_page(page: int):

        if page < 1:

            raise HTTPException(

                status_code=400,

                detail="Page must be greater than zero."

            )

    @staticmethod
    def validate_page_size(page_size: int):

        if page_size < 1 or page_size > 100:

            raise HTTPException(

                status_code=400,

                detail="Page size must be between 1 and 100."

            )

    @staticmethod
    def validate_category(category: str):

        allowed = {

            "general",

            "technology",

            "business",

            "sports",

            "science",

            "health",

            "entertainment"

        }

        if category.lower() not in allowed:

            raise HTTPException(

                status_code=400,

                detail="Invalid category."

            )