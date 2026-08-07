import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.services.api_log_service import APILogService

from app.database.database import SessionLocal


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(

        self,

        request,

        call_next

    ):

        start = time.time()

        response = await call_next(request)

        elapsed = time.time() - start

        db = SessionLocal()

        try:

            APILogService.log_request(

                db=db,

                endpoint=request.url.path,

                method=request.method,

                status=response.status_code,

                response_time=elapsed,

                client_ip=request.client.host

            )

        finally:

            db.close()

        return response