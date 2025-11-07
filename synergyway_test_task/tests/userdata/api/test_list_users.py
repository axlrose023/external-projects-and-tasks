# region            -----External Imports-----
import pytest
# endregion


@pytest.mark.django_db(transaction=True)
def test_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db(transaction=True)
def test_users_with_relations(client, user_with_relations):
    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    item = data[0]
    assert item["id"] == user_with_relations.id
    assert item["address"]["city"] == "Kyiv"
    assert item["credit_card"]["cc_number"] == "4111111111111111"
