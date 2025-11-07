import pytest

@pytest.mark.anyio
class TestAddItems:
    async def test_add_items_201(self, async_client, auth_headers, create_dataset_in_db, items_payloads, items_body_factory):
        dataset = await create_dataset_in_db(name="items_target", description="desc", items=[])
        request_body = items_body_factory(dataset_id=dataset.id, list_of_data=items_payloads)

        response_create = await async_client.post(
            f"/datasets/{dataset.id}/items/",
            json=request_body,
            headers=auth_headers,
        )
        assert response_create.status_code == 201, response_create.text

        created_items = response_create.json()
        assert isinstance(created_items, list)
        assert len(created_items) == len(items_payloads)
        for created in created_items:
            assert "id" in created
            assert created["dataset_id"] == dataset.id
            assert "data" in created

    async def test_add_items_404_when_dataset_missing(self, async_client, auth_headers, items_payloads, items_body_factory):
        missing_id = 999999
        request_body = items_body_factory(dataset_id=missing_id, list_of_data=items_payloads)

        response_create = await async_client.post(
            f"/datasets/{missing_id}/items/",
            json=request_body,
            headers=auth_headers,
        )
        assert response_create.status_code == 404, response_create.text
