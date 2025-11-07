# region            -----External Imports-----
from celery import shared_task
from celery.signals import task_success, task_failure, task_retry
from celery.utils.log import get_task_logger
# endregion

# region            -----Internal Imports-----
from ..service import UserService, AddressService, CreditCardService
# endregion

# region            -----Supporting Variables-----
logger = get_task_logger(__name__)
# endregion


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    logger.info(f"Task {sender.name} completed successfully with result: {result}")

@task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    logger.error(f"Task {sender.name} failed with error: {exception}")

@task_retry.connect
def task_retry_handler(sender=None, reason=None, **kwargs):
    logger.warning(f"Task {sender.name} is retrying due to: {reason}")

@shared_task(name="users.fetch_and_upsert", bind=True, max_retries=3)
def fetch_and_upsert_users(self):
    user_service = UserService()
    return user_service.fetch_and_upsert()

@shared_task(name="users.fill_addresses", bind=True, max_retries=3)
def fill_missing_addresses(self):
    address_service = AddressService()
    return address_service.fill_missing()

@shared_task(name="users.fill_credit_cards", bind=True, max_retries=3)
def fill_missing_credit_cards(self):
    cc_service = CreditCardService()
    return cc_service.fill_missing()