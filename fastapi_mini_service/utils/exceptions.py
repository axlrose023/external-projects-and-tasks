# region				-----External Imports-----
import fastapi
import typing
# endregion


class DetailedHTTPException(
    fastapi.HTTPException
):
    def __init__(
            self,
            status_code: int,
            error_code: str,
            detail: str | None,
            payload: typing.Dict[str, typing.Any] = None,
            headers: typing.Dict[str, str] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )

        if payload is None:
            payload = {}

        self.error_code = error_code
        self.payload = payload
