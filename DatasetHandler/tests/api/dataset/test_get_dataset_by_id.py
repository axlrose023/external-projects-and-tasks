import pytest

@pytest.mark.anyio
class TestGetDatasetById:
    async def test_ok(self, async_client, auth_headers, create_dataset_in_db, items_payloads):
        dataset = await create_dataset_in_db("by_id_ds", "desc", items_payloads[:2])

        get_response = await async_client.get(f"/datasets/{dataset.id}", headers=auth_headers)
        assert get_response.status_code == 200, get_response.text

        get_response_body = get_response.json()
        assert get_response_body["id"] == dataset.id
        assert get_response_body["name"] == "by_id_ds"
        assert get_response_body["count"] == 2

    async def test_404(self, async_client, auth_headers):
        get_response = await async_client.get("/datasets/999999", headers=auth_headers)
        assert get_response.status_code == 404
