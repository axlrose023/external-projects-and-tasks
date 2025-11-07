# region				-----External Imports-----
import celery
import logging
import asyncio
# endregion

# region				-----Internal Imports-----
from ..api.frontend.restful.service import ProductService
# endregion

# region			  -----Supporting Variables-----
logger = logging.getLogger(
    __name__
)
# endregion

@celery.shared_task(queue='basic_queue')
def refresh_all_products_task():
    service = ProductService()
    return asyncio.run(
        service.update_all_external_products()
    )
