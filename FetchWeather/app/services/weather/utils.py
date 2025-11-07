from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.repository.database.base import DatabaseRepository


def setup_task_listeners(
    scheduler: AsyncIOScheduler, database_repository: DatabaseRepository
):
    def job_success_listener(event):
        import asyncio

        asyncio.create_task(database_repository.task_log.log_success(event.retval))

    def job_error_listener(event):
        error_details = f"Job failed: {str(event.exception)}"
        import asyncio

        asyncio.create_task(
            database_repository.task_log.log_failure(None, error_details)
        )

    scheduler.add_listener(job_success_listener, EVENT_JOB_EXECUTED)
    scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)
