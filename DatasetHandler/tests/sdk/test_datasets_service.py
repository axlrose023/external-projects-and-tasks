import pytest
from sdk.fancyds.exceptions import NotFoundError

@pytest.mark.anyio
class TestDatasetsService:
    async def test_create_dataset(self, fancy_client):
        dataset = await fancy_client.datasets.create(name="sdk_ds_1", description="sdk desc")
        assert dataset.id > 0
        assert dataset.name == "sdk_ds_1"
        assert dataset.description == "sdk desc"
        assert isinstance(dataset.count, int)

    async def test_get_by_id_and_by_name(self, fancy_client):
        created = await fancy_client.datasets.create(name="sdk_ds_get", description=None)

        by_id = await fancy_client.datasets.get(created.id)
        assert by_id.id == created.id
        assert by_id.name == "sdk_ds_get"

        by_name = await fancy_client.datasets.get("sdk_ds_get")
        assert by_name.id == created.id
        assert by_name.name == "sdk_ds_get"

    async def test_iterate_all_datasets(self, fancy_client):
        await fancy_client.datasets.create(name="sdk_iter_1")
        names = set()
        async for ds in fancy_client.datasets:
            names.add(ds.name)
        assert "sdk_iter_1" in names

    async def test_filter_by_name_contains(self, fancy_client):
        await fancy_client.datasets.create(name="alpha_test_sdk")
        await fancy_client.datasets.create(name="beta_dataset")

        filtered = []
        async for ds in fancy_client.datasets.filter(name_contains="test"):
            filtered.append(ds.name)

        assert "alpha_test_sdk" in filtered
        assert "beta_dataset" not in filtered

    async def test_get_non_existing_raises_not_found(self, fancy_client):
        with pytest.raises(NotFoundError):
            await fancy_client.datasets.get(999999)
