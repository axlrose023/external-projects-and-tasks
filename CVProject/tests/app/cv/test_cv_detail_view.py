import pytest
from django.urls import reverse
from cv_app.models import CV

class TestCVDetailEndpoint:
    @pytest.mark.django_db
    def test_ok_200_and_shows_fields(self, client, sample_data):
        cv = CV.objects.first()
        resp = client.get(reverse("cv_detail", args=[cv.pk]))
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("Content-Type", "")

        body = resp.content.decode()
        assert cv.firstname in body
        assert cv.lastname in body
        if isinstance(cv.skills, (list, tuple)) and cv.skills:
            assert str(cv.skills[0]) in body

    @pytest.mark.django_db
    def test_404_for_missing_pk(self, client, sample_data):
        missing_pk = 999999
        assert not CV.objects.filter(pk=missing_pk).exists()
        resp = client.get(reverse("cv_detail", args=[missing_pk]))
        assert resp.status_code == 404

    @pytest.mark.django_db
    def test_unsupported_method_405(self, client, sample_data):
        cv = CV.objects.first()
        resp = client.post(reverse("cv_detail", args=[cv.pk]), {})
        assert resp.status_code == 405
