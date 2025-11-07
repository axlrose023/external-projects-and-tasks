import pytest
from rest_framework import status
from cv_app.models import CV


class TestV1CVCreate:
    @pytest.mark.django_db
    def test_create_ok(self, api, url_list):
        payload = {
            "firstname": "Ada",
            "lastname": "Lovelace",
            "bio": "First programmer.",
            "skills": ["Math", "Python"],
            "projects": [{"name": "Analytical Engine", "year": 1843}],
            "contacts": {"email": "ada@example.com"},
        }
        r = api.post(url_list(), payload, format="json")
        assert r.status_code == status.HTTP_201_CREATED
        new_id = r.json()["id"]
        assert CV.objects.filter(pk=new_id).exists()

    @pytest.mark.django_db
    def test_create_defaults_for_empty_collections(self, api, url_list):
        payload = {"firstname": "John", "lastname": "Doe"}
        r = api.post(url_list(), payload, format="json")
        assert r.status_code == status.HTTP_201_CREATED
        body = r.json()
        assert body["skills"] == []
        assert body["projects"] == []
        assert body["contacts"] == {}

    @pytest.mark.django_db
    def test_create_validation_errors(self, api, url_list):
        bad = {
            "firstname": "Bad",
            "lastname": "Data",
            "skills": "str",
            "projects": {"x": 1},
            "contacts": [],
        }
        r = api.post(url_list(), bad, format="json")
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        err = r.json()
        assert "skills" in err and "projects" in err and "contacts" in err
