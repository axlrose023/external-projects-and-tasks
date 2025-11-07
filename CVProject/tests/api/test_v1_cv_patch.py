import pytest
from rest_framework import status
from cv_app.models import CV

class TestV1CVPatch:
    @pytest.mark.django_db
    def test_patch_ok_partial(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        r = api.patch(url_detail(cv.pk), {"bio": "Patched"}, format="json")
        assert r.status_code == status.HTTP_200_OK
        cv.refresh_from_db()
        assert cv.bio == "Patched"

    @pytest.mark.django_db
    def test_patch_validation_error(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        r = api.patch(url_detail(cv.pk), {"skills": "oops"}, format="json")
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_patch_404(self, api, url_detail):
        r = api.patch(url_detail(999999), {"bio": "x"}, format="json")
        assert r.status_code == status.HTTP_404_NOT_FOUND
