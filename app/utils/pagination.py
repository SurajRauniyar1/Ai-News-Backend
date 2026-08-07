from math import ceil


class Pagination:

    @staticmethod
    def build(

        total: int,

        page: int,

        page_size: int

    ):

        return {

            "page": page,

            "page_size": page_size,

            "total": total,

            "total_pages": ceil(total / page_size)

        }