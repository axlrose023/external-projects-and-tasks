# region				-----External Imports-----
import fastapi

# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
api_router = fastapi.APIRouter(prefix="/api")
# endregion
from .api.frontend.restful.views import router as userdata_router