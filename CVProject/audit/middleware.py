import time
from typing import Iterable
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

IGNORED: Iterable[str] = getattr(
    settings, "REQUEST_LOG_IGNORED_PREFIXES", ("/static/", "/admin/", "/favicon.ico")
)

def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # берём первый адрес
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._audit_started_at = time.perf_counter()

    def process_response(self, request, response):
        path = request.path or "/"
        for pref in IGNORED:
            if path.startswith(pref):
                return response

        try:
            started = getattr(request, "_audit_started_at", None)
            duration_ms = int((time.perf_counter() - started) * 1000) if started else 0
            RequestLog.objects.create(
                method=request.method,
                path=path,
                query=request.META.get("QUERY_STRING", "")[:1024],
                ip=_client_ip(request),
                user=getattr(request, "user", None) if getattr(request, "user", None) and request.user.is_authenticated else None,
                status_code=getattr(response, "status_code", 0),
                duration_ms=duration_ms,
            )
        except Exception:
            pass

        return response
