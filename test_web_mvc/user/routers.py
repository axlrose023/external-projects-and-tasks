# region				-----External Imports-----
import fastapi

# endregion

# region				-----Internal Imports-----
from .api.frontend import user_router as frontend_user_router

# endregion

# region			  -----Supporting Variables-----
api_router = fastapi.APIRouter(prefix="/api")
# endregion


api_router.include_router(frontend_user_router, prefix=f"/frontend")
