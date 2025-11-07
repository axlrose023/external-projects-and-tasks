from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from schemas import (
    InitializeRequest, InitializeResponse,
    ChatRequest, ChatResponse,
    MemoryRequest, MemoryResponse
)
from dependencies import get_app_services, AppServices

router = InferringRouter()


@cbv(
    router
)
class ChatView:
    services: AppServices = Depends(
        get_app_services
    )

    @router.post(
        "/initialize",
        response_model=InitializeResponse
    )
    async def initialize_data(
            self
    ):
        count = self.services.initialize_cocktails()
        return InitializeResponse(
            status="Initialized",
            count=count
        )

    @router.post(
        "/memory",
        response_model=MemoryResponse
    )
    async def add_memory(
            self,
            payload: MemoryRequest
    ):
        self.services.memory_store_service.add_user_memory_from_payload(
            payload
        )
        return MemoryResponse(
            status="Memory added"
        )

    @router.post(
        "/chat",
        response_model=ChatResponse
    )
    async def chat(
            self,
            payload: ChatRequest
    ):
        answer = self.services.rag_pipeline_service.rag_answer(
            user_id=payload.user_id,
            query=payload.question
        )
        return ChatResponse(
            answer=answer
        )
