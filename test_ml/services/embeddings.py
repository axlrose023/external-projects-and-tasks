import openai
import numpy as np
from typing import List


class EmbeddingsService:

    def __init__(
            self,
            openai_api_key: str,
            model: str,
            embed_dim: int
    ):
        openai.api_key = openai_api_key
        self.model = model
        self.embed_dim = embed_dim

    def get_embedding(
            self,
            text: str
    ) -> List[float]:

        response = openai.Embedding.create(
            input=[text],
            model=self.model
        )
        return response["data"][0]["embedding"]

    def embed_texts(
            self,
            texts: List[str]
    ) -> np.ndarray:

        embeddings = []
        for txt in texts:
            emb = self.get_embedding(
                txt
            )
            embeddings.append(
                emb
            )
        return np.array(
            embeddings,
            dtype=np.float32
        )
