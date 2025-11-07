# region            -----External Imports-----
from __future__ import annotations
import httpx
# endregion

# region            -----Internal Imports-----
# endregion

# region            -----Supporting Variables-----
# endregion


class Requester:

    def __init__(self, timeout: int = 10) -> None:
        self._client = httpx.Client(timeout=timeout)

    def make_request(self, url: str) -> dict | list:
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()
