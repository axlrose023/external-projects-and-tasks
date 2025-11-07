import pytest
from rest_framework import status
from cv_app.models import CV

class TestV1CVDelete:
    @pytest.mark.django_db
    def test_delete_ok(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        r = api.delete(url_detail(cv.pk))
        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert not CV.objects.filter(pk=cv.pk).exists()

    @pytest.mark.django_db
    def test_delete_twice_second_404(self, api, sample_data, url_detail):
        cv = CV.objects.first()
        api.delete(url_detail(cv.pk))
        r2 = api.delete(url_detail(cv.pk))
        assert r2.status_code == status.HTTP_404_NOT_FOUND
