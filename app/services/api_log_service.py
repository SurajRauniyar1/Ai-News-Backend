from app.models.api_log import APILog


class APILogService:

    @staticmethod
    def log_request(

        db,

        endpoint,

        method,

        status,

        response_time,

        client_ip

    ):

        log = APILog(

            endpoint=endpoint,

            method=method,

            status_code=status,

            response_time=response_time,

            client_ip=client_ip

        )

        db.add(log)

        db.commit()

        db.refresh(log)

        return log