import asyncio
from sdk.fancyds.client import FancyDataClient
from sdk.fancyds.exceptions import FancyDataError, APIError


class DatasetTest:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def run(self):
        async with FancyDataClient(
            api_url=self.api_url,
            api_key=self.api_key
        ) as client:
            await self.test_create_dataset(client)
            await self.test_get_dataset_by_id(client)
            await self.test_list_all_datasets(client)
            await self.test_filter_datasets(client)
            await self.test_manage_items(client)
            await self.test_get_non_existent_dataset(client)

    async def test_create_dataset(self, client):
        try:
            ds = await client.datasets.create(
                name="manual_test_ds", description="Test description"
            )
            print(
                f"Created dataset: ID={ds.id}, Name={ds.name}, Count={ds.count}"
            )
        except FancyDataError as e:
            print(f"Dataset creation error: {e}")

    async def test_get_dataset_by_id(self, client):
        try:
            ds_by_id = await client.datasets.get(1)
            print(
                f"Retrieved dataset by ID: Name={ds_by_id.name}, Count="
                f"{ds_by_id.count}"
            )
        except APIError as e:
            print(f"Error retrieving by ID: {e}")

    async def test_list_all_datasets(self, client):
        print("All datasets:")
        async for ds in client.datasets:
            print(f"- ID={ds.id}, Name={ds.name}, Count={ds.count}")

    async def test_filter_datasets(self, client):
        print("Filtered datasets (containing 'test'):")
        async for ds in client.datasets.filter(name_contains="test"):
            print(f"- ID={ds.id}, Name={ds.name}")

    async def test_manage_items(self, client):
        try:
            ds = await client.datasets.get(1)
            items = ds.items

            await items.add(
                {
                    "key": "value1",
                    "num": 42
                }
            )
            print("Added one item")

            batch = [{
                         "key": "value2"}, {
                         "key": "value3"}]
            await items.add_batch(batch)
            print(
                f"Added batch of {len(batch)} items. New count: {ds.count}"
            )

            print("All items:")
            async for item in items:
                print(item)

            print("Filtered items (num >= 40):")
            async for item in items.filter(num__gte=40):
                print(item)
        except ValueError as e:
            print(f"Error with items: {e}")

    async def test_get_non_existent_dataset(self, client):
        try:
            await client.datasets.get(999999)
        except APIError as e:
            print(f"Expected error (Not Found): {e}")


if __name__ == "__main__":
    test = DatasetTest(
        api_url="http://localhost:8000/api",
        api_key="83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
    )
    asyncio.run(test.run())