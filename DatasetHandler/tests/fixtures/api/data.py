import pytest
from app.models.dataset import Dataset, Item

@pytest.fixture
def dataset_payload():
    return {"name": "ds_one", "description": "first dataset"}

@pytest.fixture
def another_dataset_payload():
    return {"name": "ds_two", "description": "second dataset"}

@pytest.fixture
def items_payloads():
    return [{"x": 1}, {"x": 2}, {"x": 3}]

@pytest.fixture
def create_dataset_in_db(session_maker):
    async def _create(name: str, description: str | None = None, items: list[dict] | None = None) -> Dataset:
        async with session_maker() as session:
            dataset = Dataset(name=name, description=description)
            session.add(dataset)
            await session.flush()
            if items:
                for data in items:
                    session.add(Item(dataset_id=dataset.id, data=data))
            await session.commit()
            await session.refresh(dataset)
            return dataset
    return _create

@pytest.fixture
def items_body_factory():
    def _build(dataset_id: int, list_of_data: list[dict]):
        return [{"dataset_id": dataset_id, "data": data} for data in list_of_data]
    return _build
