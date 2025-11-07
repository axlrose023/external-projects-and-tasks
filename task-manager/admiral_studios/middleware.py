import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        method = request.method
        path = request.get_full_path()
        status_code = response.status_code

        logger.info(
            f"[{method}] {path} - {status_code} - {duration:.3f}s"
        )
        return response
