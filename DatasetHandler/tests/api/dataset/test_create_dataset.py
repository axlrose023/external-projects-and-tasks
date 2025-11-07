import pytest

@pytest.mark.anyio
class TestCreateDataset:
    async def test_create_201(self, async_client, auth_headers, dataset_payload):
        create_response = await async_client.post("/datasets/", json=dataset_payload, headers=auth_headers)
        assert create_response.status_code == 201, create_response.text

        create_response_body = create_response.json()
        assert create_response_body["id"] > 0
        assert create_response_body["name"] == dataset_payload["name"]
        assert create_response_body["description"] == dataset_payload["description"]
        assert create_response_body["count"] == 0

    async def test_create_duplicate(self, async_client, auth_headers, dataset_payload):
        first_create_response = await async_client.post("/datasets/", json=dataset_payload, headers=auth_headers)
        assert first_create_response.status_code == 201, first_create_response.text

        duplicate_create_response = await async_client.post("/datasets/", json=dataset_payload, headers=auth_headers)
        assert duplicate_create_response.status_code in (400, 409), duplicate_create_response.text
