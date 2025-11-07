import pytest

@pytest.mark.anyio
class TestGetDatasetByName:
    async def test_ok(self, async_client, auth_headers, create_dataset_in_db, items_payloads):
        dataset = await create_dataset_in_db("by_name_ds", "desc", items_payloads)

        get_by_name_response = await async_client.get(f"/datasets/name/{dataset.name}", headers=auth_headers)
        assert get_by_name_response.status_code == 200, get_by_name_response.text

        get_by_name_body = get_by_name_response.json()
        assert get_by_name_body["id"] == dataset.id
        assert get_by_name_body["name"] == "by_name_ds"
        assert get_by_name_body["count"] == 3

    async def test_404(self, async_client, auth_headers):
        get_by_name_response = await async_client.get("/datasets/name/not_exists", headers=auth_headers)
        assert get_by_name_response.status_code == 404
