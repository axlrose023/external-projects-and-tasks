import pytest
from rest_framework import status
from cv_app.models import CV

class TestV1CVRetrieve:
    @pytest.mark.django_db
    def test_retrieve_ok(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        r = api.get(url_detail(cv.pk))
        assert r.status_code == status.HTTP_200_OK
        body = r.json()
        assert body["id"] == cv.pk
        assert body["firstname"] == cv.firstname
        assert body["lastname"] == cv.lastname

    @pytest.mark.django_db
    def test_retrieve_404(self, api, sample_data, url_detail):
        r = api.get(url_detail(999999))
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_retrieve_types(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        r = api.get(url_detail(cv.pk))
        body = r.json()
        assert isinstance(body["skills"], list)
        assert isinstance(body["projects"], list)
        assert isinstance(body["contacts"], dict)
