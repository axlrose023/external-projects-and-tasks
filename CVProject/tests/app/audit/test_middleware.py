import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from audit.models import RequestLog
import audit.middleware as mw


class TestRequestLoggingMiddleware:
    @pytest.mark.django_db
    def test_logs_any_request(self, client):
        resp = client.get("/audit/logs/")
        assert resp.status_code in (200, 301, 302)
        assert RequestLog.objects.filter(path="/audit/logs/").exists()

    @pytest.mark.django_db
    def test_logs_status_code_and_duration(self, client):
        client.get("/logs")
        log = RequestLog.objects.order_by("-timestamp").first()
        assert log is not None
        assert isinstance(log.status_code, int) and log.status_code >= 0
        assert isinstance(log.duration_ms, int) and log.duration_ms >= 0

    @pytest.mark.django_db
    def test_ignored_prefix_is_not_logged(self, client, monkeypatch):
        monkeypatch.setattr(mw, "IGNORED", ("/static/",))
        client.get("/static/style.css")
        assert not RequestLog.objects.filter(path="/static/style.css").exists()

    @pytest.mark.django_db
    def test_user_may_be_logged_if_authenticated(self, client):
        User = get_user_model()
        user = User.objects.create_user(username="u1", password="p")
        assert client.login(username="u1", password="p")
        client.get("/logs")
        log = RequestLog.objects.order_by("-timestamp").first()
        assert log is not None
        assert (log.user_id is None) or (log.user_id == user.id)
