import math


AVERAGE_WPM = 200


def calculate_reading_time(content: str):

    if not content:

        return 1

    words = len(content.split())

    return max(

        1,

        math.ceil(

            words / AVERAGE_WPM

        ),

    )