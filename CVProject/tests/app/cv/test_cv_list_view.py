import re
import pytest
from django.urls import reverse
from cv_app.models import CV

class TestCVListEndpoint:
    @pytest.mark.django_db
    def test_ok_200_html_and_total_and_name(self, client, sample_data):
        resp = client.get(reverse("cv_list"))
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("Content-Type", "")
        body = resp.content.decode()

        total = CV.objects.count()
        assert str(total) in body

        cv = CV.objects.first()
        assert f"{cv.lastname} {cv.firstname}" in body

    @pytest.mark.django_db
    def test_ordering_lastname_then_firstname(self, client, sample_data):
        first = CV.objects.create(
            firstname="Bob",
            lastname="Aardvark",
            bio="",
            skills=[],
            projects=[],
            contacts={},
        )

        resp = client.get(reverse("cv_list"))
        assert resp.status_code == 200
        html = resp.content.decode("utf-8")

        items = list(resp.context["items"])
        assert items[0].pk == first.pk

        m = re.search(
            r'<div class="name">\s*(?:<a[^>]*>)?([^<]+?)(?:</a>)?\s*</div>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        assert m, "Cannot find first .name block in HTML"
        first_rendered = " ".join(m.group(1).split())
        assert first_rendered.startswith("Aardvark") and "Bob" in first_rendered

    @pytest.mark.django_db
    def test_empty_state_without_fixture(self, client):
        resp = client.get(reverse("cv_list"))
        assert resp.status_code == 200
        assert resp.context["total"] == 0
        assert list(resp.context["items"]) == []
        assert "No records yet." in resp.content.decode()

    @pytest.mark.django_db
    def test_unsupported_method_405(self, client, sample_data):
        resp = client.post(reverse("cv_list"), {})
        assert resp.status_code == 405
