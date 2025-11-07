from typing import Callable
import pytest
from django.urls import reverse

@pytest.fixture
def url_list() -> Callable[[], str]:
    def _url() -> str:
        return reverse("v1:cv-list")
    return _url

@pytest.fixture
def url_detail() -> Callable[[int], str]:
    def _url(pk: int) -> str:
        return reverse("v1:cv-detail", args=[pk])
    return _url
