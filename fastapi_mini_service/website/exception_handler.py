# region				-----External Imports-----
import fastapi
from utils import exceptions as utils_exceptions

# endregion
# region				-----Internal Imports-----
# endregion


async def detailed_exception_handler(
    request: fastapi.Request,
    exc: utils_exceptions.DetailedHTTPException,
):
    return fastapi.responses.JSONResponse(
        content={
            "code": exc.error_code,
            "payload": exc.payload,
            "detail": exc.detail,
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )