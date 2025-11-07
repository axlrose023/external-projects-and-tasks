import pytest
from rest_framework import status
from cv_app.models import CV

class TestV1CVUpdatePut:
    @pytest.mark.django_db
    def test_put_ok_overwrites_all(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        payload = {
            "firstname": "Alan",
            "lastname": "Turing",
            "bio": "Updated",
            "skills": ["Crypto"],
            "projects": [{"name": "Bombe"}],
            "contacts": {"email": "alan@example.com"},
        }
        r = api.put(url_detail(cv.pk), payload, format="json")
        assert r.status_code == status.HTTP_200_OK
        cv.refresh_from_db()
        assert cv.firstname == "Alan"
        assert cv.skills == ["Crypto"]
        assert cv.projects and cv.projects[0]["name"] == "Bombe"

    @pytest.mark.django_db
    def test_put_404(self, api, url_detail):
        payload = {
            "firstname": "X", "lastname": "Y",
            "skills": [], "projects": [], "contacts": {}
        }
        r = api.put(url_detail(999999), payload, format="json")
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_put_validation_error(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        payload = {"firstname": "A", "lastname": "B", "skills": "oops", "projects": {}, "contacts": []}
        r = api.put(url_detail(cv.pk), payload, format="json")
        assert r.status_code == status.HTTP_400_BAD_REQUEST
