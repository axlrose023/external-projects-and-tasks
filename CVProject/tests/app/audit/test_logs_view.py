import pytest
from django.urls import reverse
from audit.models import RequestLog


class TestRecentLogsView:
    @pytest.mark.django_db
    def test_renders_last_10_desc(self, client):
        RequestLog.objects.bulk_create([
            RequestLog(method="GET", path=f"/p/{i}", status_code=200)
            for i in range(12)
        ])

        resp = client.get(reverse("logs"))
        assert resp.status_code == 200
        logs = list(resp.context["logs"])
        assert len(logs) == 10
        assert logs[0].path == "/p/11"
        assert logs[-1].path == "/p/2"

    @pytest.mark.django_db
    def test_empty_state(self, client):
        resp = client.get(reverse("logs"))
        assert resp.status_code == 200
        assert list(resp.context["logs"]) == []
        assert "No entries yet." in resp.content.decode()

    @pytest.mark.django_db
    def test_items_contain_method_path_and_status(self, client):
        RequestLog.objects.create(method="POST", path="/cv/1/", status_code=201)
        resp = client.get(reverse("logs"))
        assert resp.status_code == 200
        html = resp.content.decode()
        assert "POST" in html
        assert "/cv/1/" in html
        assert "201" in html
