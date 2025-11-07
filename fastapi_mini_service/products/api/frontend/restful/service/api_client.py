# region				-----External Imports-----
import httpx
from utils.exceptions import DetailedHTTPException
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
BASE_URL = "https://fakestoreapi.com/products"
# endregion


class ExternalProductAPIClient:

    async def __aenter__(
            self
    ):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(
            self,
            exc_type,
            exc_value,
            traceback
    ):
        await self.client.aclose()

    async def fetch_product(
            self,
            product_id: int
    ) -> dict:
        url = f"{BASE_URL}/{product_id}"
        try:
            response = await self.client.get(
                url
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as error:
            status_code = error.response.status_code if error.response else 500
            response_body = await error.response.aread() if error.response \
                else "No Response"

            raise DetailedHTTPException(
                status_code=status_code,
                error_code="REQUEST_FAILED",
                detail=f"Failed request to {url}: {str(error)}. Response "
                       f"body: {response_body}"
            ) from error
