from settings import Settings
from services.csv_loader import CSVLoaderService
from services.embeddings import EmbeddingsService
from services.llm_client import LLMClientService
from services.memory_store import MemoryStoreService
from services.rag_pipeline import RAGPipelineService


class AppServices:
    def __init__(
            self
    ):
        settings = Settings()
        self.csv_loader_service = CSVLoaderService()
        self.embeddings_service = EmbeddingsService(
            openai_api_key=settings.openai_api_key,
            model=settings.embed_model,
            embed_dim=settings.embed_dim
        )
        self.memory_store_service = MemoryStoreService(
            self.embeddings_service
        )
        self.llm_client_service = LLMClientService(
            openai_api_key=settings.openai_api_key,
            model=settings.llm_model
        )
        self.rag_pipeline_service = RAGPipelineService(
            memory_store_service=self.memory_store_service,
            llm_client_service=self.llm_client_service
        )
        self.csv_file_path = settings.csv_file_path

    def initialize_cocktails(
            self
    ) -> int:
        self.memory_store_service.reset_global_cocktails()
        cocktails = self.csv_loader_service.load_cocktails_from_csv(
            self.csv_file_path
        )
        texts = [c["text"] for c in cocktails]
        metadata = [{
            "id": c["id"],
            "name": c["name"]
        } for c in cocktails]
        self.memory_store_service.add_to_global_cocktails(
            texts,
            metadata
        )
        return len(
            cocktails
        )


def get_app_services():
    return AppServices()
