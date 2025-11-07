import pytest
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000"


@pytest.fixture(
    scope="session"
)
def session():
    with requests.Session() as s:
        yield s


@pytest.mark.parametrize(
    "endpoint, expected_status",
    [
        ("/docs", 200),
        ("/nonexistent", 404),
    ]
)
def test_endpoint_status_codes(
        session,
        endpoint,
        expected_status
):
    response = session.get(
        f"{BASE_URL}{endpoint}"
    )
    assert response.status_code == expected_status, (
        f"For endpoint '{endpoint}', expected {expected_status} but got "
        f"{response.status_code}"
    )


def test_response_headers_and_body(
        session
):

    response = session.get(
        f"{BASE_URL}/docs"
    )
    assert "Content-Type" in response.headers, (
        "Missing 'Content-Type' header "
        "in response"
    )
    content_type = response.headers["Content-Type"]
    assert "text/html" in content_type or "application/json" in content_type, (
        f"Unexpected Content-Type: {content_type}"
    )
    assert response.text.strip() != "", "Response body is empty"


def test_head_method(
        session
):

    response = session.head(
        f"{BASE_URL}/docs"
    )
    assert response.status_code == 200, (f"HEAD request returned status "
                                         f"{response.status_code}")
    assert response.text == "", "HEAD response should not include a body"


def test_concurrent_requests(
        session
):

    endpoints = ["/docs" for _ in range(
        10
    )]
    start_time = time.time()
    with ThreadPoolExecutor(
            max_workers=10
    ) as executor:
        futures = [executor.submit(
            session.get,
            f"{BASE_URL}{endpoint}"
        ) for endpoint in endpoints]
        responses = [future.result() for future in as_completed(
            futures
        )]
    elapsed_time = time.time() - start_time

    for response in responses:
        assert response.status_code == 200, (
            f"Concurrent request returned status code {response.status_code}"
        )
    assert elapsed_time < 3, (
        f"Concurrent requests took too long: "
        f"{elapsed_time:.2f} seconds"
    )


def test_invalid_method(
        session
):

    response = session.put(
        f"{BASE_URL}/docs"
    )
    assert response.status_code != 200, (
        "PUT request unexpectedly returned "
        "status 200"
    )


def test_response_time_threshold(
        session
):

    response = session.get(
        f"{BASE_URL}/docs"
    )
    elapsed = response.elapsed.total_seconds()
    threshold = 0.5
    assert elapsed < threshold, (
        f"Response time is too high: {elapsed:.2f} "
        f"seconds"
    )
