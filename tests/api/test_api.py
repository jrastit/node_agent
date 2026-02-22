from tests.utils.api_util import api_client


def test_api_auth():
    """
    GIVEN an API application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = api_client.get("/api/test/ping")
    assert response.status_code == 401
    response = api_client.get(
        "/api/test/ping",
        headers={
            "Grpc-Metadata-Authorization": "error",
        },
    )
    assert response.status_code == 401
