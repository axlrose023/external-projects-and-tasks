import pytest
import pandas as pd

@pytest.mark.anyio
class TestItemsService:
    async def test_add_single_and_list_back(self, fancy_client):
        ds = await fancy_client.datasets.create(name="sdk_items_single")
        await ds.items.add({"name": "Alice", "age": 30})

        items = []
        async for item in ds.items:
            items.append(item)
        assert any(i.get("name") == "Alice" and i.get("age") == 30 for i in items)

    async def test_add_batch_returns_item_responses(self, fancy_client):
        ds = await fancy_client.datasets.create(name="sdk_items_batch")

        batch = [
            {"name": "Bob", "age": 25},
            {"name": "Carol", "age": 41},
        ]
        responses = await ds.items.add_batch(batch)
        assert isinstance(responses, list)
        assert len(responses) == 2
        assert all(r.dataset_id == ds.id for r in responses)
        assert all(hasattr(r, "id") for r in responses)

    async def test_add_from_pandas_and_iterate(self, fancy_client):
        ds = await fancy_client.datasets.create(name="sdk_items_pandas")

        df = pd.DataFrame([
            {"name": "D1", "age": 20},
            {"name": "D2", "age": 21},
        ])
        await ds.items.add_from_pandas(df)

        seen = []
        async for item in ds.items:
            seen.append(item["name"])
        assert {"D1", "D2"}.issubset(set(seen))

    async def test_iter_batches(self, fancy_client):
        ds = await fancy_client.datasets.create(name="sdk_items_batches")
        await ds.items.add_batch([{"idx": i} for i in range(5)])

        batches = []
        async for batch in ds.items.iter_batches(batch_size=2):
            batches.append(batch)

        assert len(batches) == 3
        total = sum(len(b) for b in batches)
        assert total == 5

    async def test_filter_gte(self, fancy_client):
        ds = await fancy_client.datasets.create(name="sdk_items_filter")
        await ds.items.add_batch([
            {"num": 10},
            {"num": 40},
            {"num": 50},
        ])

        filtered = []
        async for item in ds.items.filter(num__gte=40):
            filtered.append(item["num"])

        assert set(filtered) == {40, 50}
