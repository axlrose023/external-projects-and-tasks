# region            -----External Imports-----
from typing import ClassVar

from fastapi import APIRouter
from fastapi_restful.cbv import cbv
# endregion

# region            -----Internal Imports-----
from ..schemas import UserResponseSchema
from ..service import UserQueryService
# endregion

# region            -----Supporting Variables-----
router = APIRouter(prefix="/users", tags=["users"])
# endregion

@cbv(router)
class UserView:
    query_service: ClassVar[UserQueryService] = UserQueryService()

    @router.get("/", response_model=list[UserResponseSchema])
    async def list_users(self):
        return await self.query_service.fetch_all()
