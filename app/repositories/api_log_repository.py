from sqlalchemy.orm import Session

from app.models.api_log import APILog


class APILogRepository:

    @staticmethod
    def create(

        db: Session,

        log: APILog

    ):

        db.add(log)

        db.commit()

        db.refresh(log)

        return log

    @staticmethod
    def get_logs(

        db: Session,

        limit: int = 100

    ):

        return (

            db.query(APILog)

            .order_by(

                APILog.created_at.desc()

            )

            .limit(limit)

            .all()

        )