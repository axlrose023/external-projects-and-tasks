import pytest

@pytest.mark.anyio
class TestGetItems:
    async def test_get_items_default_pagination(self, async_client, auth_headers, create_dataset_in_db, items_payloads):
        dataset = await create_dataset_in_db(name="items_list_ds", description=None, items=items_payloads)

        response_get = await async_client.get(
            f"/datasets/{dataset.id}/items/",
            headers=auth_headers,
        )
        assert response_get.status_code == 200, response_get.text

        items = response_get.json()
        assert isinstance(items, list)
        assert len(items) == len(items_payloads)
        for item in items:
            assert item["dataset_id"] == dataset.id
            assert "id" in item
            assert "data" in item

    async def test_get_items_with_limit_and_offset(self, async_client, auth_headers, create_dataset_in_db):
        data_entries = [{"n": n} for n in range(5)]
        dataset = await create_dataset_in_db(name="items_paginated_ds", description=None, items=data_entries)

        response_get = await async_client.get(
            f"/datasets/{dataset.id}/items/?limit=2&offset=1",
            headers=auth_headers,
        )
        assert response_get.status_code == 200, response_get.text

        items = response_get.json()
        assert len(items) == 2
        for item in items:
            assert item["dataset_id"] == dataset.id

    async def test_get_items_404_when_dataset_missing(self, async_client, auth_headers):
        response_get = await async_client.get(
            "/datasets/999999/items/",
            headers=auth_headers,
        )
        assert response_get.status_code == 404, response_get.text

    async def test_get_items_422_on_invalid_query_params(self, async_client, auth_headers, create_dataset_in_db):
        dataset = await create_dataset_in_db(name="items_params_ds", description=None, items=[{"a": 1}])

        response_limit_invalid = await async_client.get(
            f"/datasets/{dataset.id}/items/?limit=0",
            headers=auth_headers,
        )
        assert response_limit_invalid.status_code == 422

        response_offset_invalid = await async_client.get(
            f"/datasets/{dataset.id}/items/?offset=-1",
            headers=auth_headers,
        )
        assert response_offset_invalid.status_code == 422
