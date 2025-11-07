import pytest
from rest_framework import status
from cv_app.models import CV

class TestV1CVList:
    @pytest.mark.django_db
    def test_list_ok_status_and_json(self, api, sample_data, url_list):
        r = api.get(url_list())
        assert r.status_code == status.HTTP_200_OK
        data = r.json()
        assert isinstance(data, list)

    @pytest.mark.django_db
    def test_list_count_matches_db(self, api, sample_data, url_list):
        r = api.get(url_list())
        assert len(r.json()) == CV.objects.count()

    @pytest.mark.django_db
    def test_list_has_expected_fields(self, api, sample_data, url_list):
        r = api.get(url_list())
        obj = r.json()[0]
        assert {"id", "firstname", "lastname", "bio", "skills", "projects", "contacts"} <= obj.keys()

    @pytest.mark.django_db
    def test_list_ordering_lastname_firstname(self, api, sample_data, url_list):
        a = CV.objects.create(firstname="Bob", lastname="Aardvark")
        b = CV.objects.create(firstname="Ann", lastname="Zebra")
        r = api.get(url_list())
        ids = [item["id"] for item in r.json()]
        assert ids[0] == a.id
        assert ids.index(a.id) < ids.index(b.id)

    @pytest.mark.django_db
    def test_list_empty(self, api, url_list):
        r = api.get(url_list())
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == []
