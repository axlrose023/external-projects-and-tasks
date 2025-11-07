from .memory_store import MemoryStoreService
from .llm_client import LLMClientService


class RAGPipelineService:
    def __init__(
            self,
            memory_store_service: MemoryStoreService,
            llm_client_service: LLMClientService
    ):
        self.memory = memory_store_service
        self.llm = llm_client_service

    def build_rag_context(
            self,
            user_id: str,
            query: str,
            top_k: int = 3
    ) -> str:
        # 1) Retrieve from global cocktails
        cocktails_info = self.memory.search_cocktails(
            query,
            k=top_k
        )
        # 2) Retrieve from user store
        user_mem = self.memory.search_user_memory(
            user_id,
            query,
            k=top_k
        )

        context_parts = []
        context_parts.append(
            "=== Cocktails Knowledge ==="
        )
        for c in cocktails_info:
            context_parts.append(
                f"- {c['text']} (score={c['score']:.2f})"
            )

        context_parts.append(
            "=== User Memory ==="
        )
        for m in user_mem:
            context_parts.append(
                f"- {m['text']} (score={m['score']:.2f})"
            )

        return "\n".join(
            context_parts
        )

    def rag_answer(
            self,
            user_id: str,
            query: str
    ) -> str:
        context = self.build_rag_context(
            user_id,
            query
        )
        prompt = f"""
            Use the following context to answer the user's question about 
            cocktails.
            If something is not found in the context, rely on general 
            knowledge, 
            but prefer context.
            
            Context:
            {context}
            
            User query: {query}
            
            Answer:
                """
        return self.llm.generate_answer(
            prompt
        )
