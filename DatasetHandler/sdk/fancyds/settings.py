from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    api_base_url: str
    api_key: str

    datasets_list_endpoint: str = "/datasets"
    datasets_create_endpoint: str = "/datasets/"
    datasets_get_by_id_endpoint: str = "/datasets/{id}/"
    datasets_get_by_name_endpoint: str = "/datasets/name/{name}/"
    items_endpoint: str = "/datasets/{dataset_id}/items/"
    items_batch_endpoint: str = "/datasets/{dataset_id}/items/"