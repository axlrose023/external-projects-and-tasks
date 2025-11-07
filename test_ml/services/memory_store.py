# services/memory_store.py
import faiss
import numpy as np
from typing import List, Dict
from services.embeddings import EmbeddingsService
from schemas import MemoryRequest


class FAISSStore:
    def __init__(
            self,
            dimension: int
    ):
        self.index = faiss.IndexFlatIP(
            dimension
        )
        self.texts = []
        self.metadata = []

    def reset(
            self
    ):
        self.index.reset()
        self.texts.clear()
        self.metadata.clear()

    def add_texts(
            self,
            vectors: np.ndarray,
            texts: List[str],
            metas: List[Dict]
    ):
        self.index.add(
            vectors
        )
        self.texts.extend(
            texts
        )
        self.metadata.extend(
            metas
        )

    def search(
            self,
            query_vector: np.ndarray,
            k: int = 3
    ):
        D, I = self.index.search(
            query_vector,
            k
        )
        results = []
        for dist_list, idx_list in zip(
                D,
                I
        ):
            for dist, idx in zip(
                    dist_list,
                    idx_list
            ):
                if idx < len(
                        self.texts
                ):
                    results.append(
                        {
                            "text": self.texts[idx],
                            "metadata": self.metadata[idx],
                            "score": float(
                                dist
                            )
                        }
                    )
        return results


class MemoryStoreService:
    def __init__(
            self,
            embeddings_service: EmbeddingsService
    ):
        self.embeddings_service = embeddings_service
        self.global_cocktails_store = FAISSStore(
            dimension=embeddings_service.embed_dim
        )
        self.user_stores: Dict[str, FAISSStore] = {}

    def reset_global_cocktails(
            self
    ):
        self.global_cocktails_store.reset()

    def add_to_global_cocktails(
            self,
            texts: List[str],
            metas: List[Dict]
    ):
        vectors = self.embeddings_service.embed_texts(
            texts
        )
        self.global_cocktails_store.add_texts(
            vectors,
            texts,
            metas
        )

    def search_cocktails(
            self,
            query: str,
            k: int = 3
    ):
        query_vec = self.embeddings_service.embed_texts(
            [query]
        )
        return self.global_cocktails_store.search(
            query_vec,
            k=k
        )

    def get_user_store(
            self,
            user_id: str
    ) -> FAISSStore:
        if user_id not in self.user_stores:
            self.user_stores[user_id] = FAISSStore(
                dimension=self.embeddings_service.embed_dim
            )
        return self.user_stores[user_id]

    def add_user_memory(
            self,
            user_id: str,
            memory_texts: List[str],
            metas: List[Dict]
    ):
        store = self.get_user_store(
            user_id
        )
        vectors = self.embeddings_service.embed_texts(
            memory_texts
        )
        store.add_texts(
            vectors,
            memory_texts,
            metas
        )

    def add_user_memory_from_payload(
            self,
            payload: MemoryRequest
    ):

        self.add_user_memory(
            user_id=payload.user_id,
            memory_texts=[payload.memory_text],
            metas=[{
                "source": "user_memory"
            }]
        )

    def search_user_memory(
            self,
            user_id: str,
            query: str,
            k: int = 3
    ):
        store = self.get_user_store(
            user_id
        )
        query_vec = self.embeddings_service.embed_texts(
            [query]
        )
        return store.search(
            query_vec,
            k=k
        )
