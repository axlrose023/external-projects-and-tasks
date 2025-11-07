from django.views.generic import ListView
from .models import RequestLog

class RecentLogsView(ListView):
    model = RequestLog
    template_name = "audit/logs.html"
    context_object_name = "logs"
    paginate_by = 20

    def get_queryset(self):
        return (
            RequestLog.objects
            .only("timestamp", "method", "path", "status_code")
            .order_by("-timestamp")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total"] = RequestLog.objects.count()
        return ctx
