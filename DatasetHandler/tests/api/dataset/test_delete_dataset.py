import pytest

@pytest.mark.anyio
class TestDeleteDataset:
    async def test_delete_then_404(self, async_client, auth_headers, create_dataset_in_db):
        dataset = await create_dataset_in_db("to_delete", "desc", [])

        delete_response = await async_client.delete(f"/datasets/{dataset.id}", headers=auth_headers)
        assert delete_response.status_code == 204, delete_response.text

        get_after_delete_response = await async_client.get(f"/datasets/{dataset.id}", headers=auth_headers)
        assert get_after_delete_response.status_code == 404
