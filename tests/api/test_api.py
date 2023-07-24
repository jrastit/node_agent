from tests.utils.api_util import flask_app


def test_api_auth():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/test/ping')
        assert response.status_code == 401
        response = test_client.get(
            '/api/test/ping',
            headers={
                'Grpc-Metadata-Authorization' : 'error',
            },
        )
        assert response.status_code == 401

