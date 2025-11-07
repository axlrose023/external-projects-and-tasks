from django.urls import path
from .views import RecentLogsView

urlpatterns = [
    path("logs/", RecentLogsView.as_view(), name="logs"),
]
