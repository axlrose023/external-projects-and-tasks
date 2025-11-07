# region            -----External Imports-----
import pytest
from fastapi.testclient import TestClient
# endregion

# region            -----Internal Imports-----
from website.asgi import app as fastapi_app
from userdata.models import User, Address, CreditCard
# endregion


@pytest.fixture(scope="session")
def client():
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture
def user_with_relations(db):
    user = User.objects.create(
        ext_id=101,
        name="John Doe",
        username="jdoe",
        email="john@example.com",
        phone="+380991112233",
        website="example.com",
    )
    Address.objects.create(
        user=user,
        city="Kyiv",
        street="Main",
        building_number="1A",
        zip_code="02000",
    )
    CreditCard.objects.create(
        user=user,
        cc_number="4111111111111111",
        cc_type="visa",
        exp_date="2030-12-01",
    )
    return user
