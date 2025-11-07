import pytest

@pytest.mark.anyio
class TestListDatasets:
    async def test_list_empty(self, async_client, auth_headers):
        list_response = await async_client.get("/datasets/", headers=auth_headers)
        assert list_response.status_code == 200

        list_response_body = list_response.json()
        assert list_response_body == []

    async def test_list_with_counts(self, async_client, auth_headers, create_dataset_in_db, items_payloads):
        await create_dataset_in_db("list_ds1", "no items", [])
        await create_dataset_in_db("list_ds2", "with items", items_payloads)

        list_response = await async_client.get("/datasets/", headers=auth_headers)
        assert list_response.status_code == 200

        datasets_list = list_response.json()
        assert len(datasets_list) == 2

        datasets_by_name = {dataset_row["name"]: dataset_row for dataset_row in datasets_list}
        assert datasets_by_name["list_ds1"]["count"] == 0
        assert datasets_by_name["list_ds2"]["count"] == 3
