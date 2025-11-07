# region				-----External Imports-----
import fastapi

# endregion

# region				-----Internal Imports-----
from .api.frontend.restful.views import post_router
# endregion

# region			  -----Supporting Variables-----
api_router = fastapi.APIRouter(prefix="/api")
# endregion

api_router.include_router(post_router)
