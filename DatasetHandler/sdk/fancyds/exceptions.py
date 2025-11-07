from typing import Optional

import httpx

class FancyDataError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)

class APIError(FancyDataError):
    """General API-related error."""

class AuthenticationError(APIError):
    """Authentication failed (e.g., invalid API key)."""

class NotFoundError(APIError):
    """Resource not found (e.g., dataset or item)."""

class ValidationError(APIError):
    """Input validation error."""

class RateLimitError(APIError):
    """API rate limit exceeded."""

def handle_api_error(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        try:
            error_data = exc.response.json()
            message = error_data.get("detail", str(exc))
        except ValueError:
            message = str(exc)

        if status_code == 401:
            raise AuthenticationError(f"Authentication failed: {message}", status_code, error_data)
        elif status_code == 404:
            raise NotFoundError(f"Resource not found: {message}", status_code, error_data)
        elif status_code == 422:
            raise ValidationError(f"Validation error: {message}", status_code, error_data)
        elif status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {message}", status_code, error_data)
        else:
            raise APIError(f"API error: {message}", status_code, error_data)