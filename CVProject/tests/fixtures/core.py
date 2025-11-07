import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

@pytest.fixture
def sample_data(db):
    call_command("loaddata", "cv")

@pytest.fixture
def api() -> APIClient:
    return APIClient()

