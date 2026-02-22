from fastapi.testclient import TestClient

from tests.conftest import init_app

app = init_app()
api_client = TestClient(app)


def _json_or_none(response):
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        return None
    return response.json()


def api_get(url, status_code, params):
    response = api_client.get(
        url,
        headers={"Grpc-Metadata-Authorization": "Bearer test"},
        params=params,
    )
    assert response.status_code == status_code, (
        "status code : " + str(response.status_code) + " " + response.text
    )
    return _json_or_none(response)


def api_simple_get(url, status_code):
    response = api_client.get(
        url, headers={"Grpc-Metadata-Authorization": "Bearer test"}
    )
    assert response.status_code == status_code, (
        "status code : " + str(response.status_code) + " " + response.text
    )
    return _json_or_none(response)


def api_simple_delete(url, status_code):
    response = api_client.delete(
        url, headers={"Grpc-Metadata-Authorization": "Bearer test"}
    )
    assert response.status_code == status_code, (
        "status code : " + str(response.status_code) + " " + response.text
    )
    return _json_or_none(response)


def api_simple_post(url, status_code):
    response = api_client.post(
        url, headers={"Grpc-Metadata-Authorization": "Bearer test"}
    )
    assert response.status_code == status_code
    return _json_or_none(response)


def api_post_data(url, status_code, data):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype,
        "Grpc-Metadata-Authorization": "Bearer test",
    }
    response = api_client.post(url, headers=headers, json=data)
    assert response.status_code == status_code
    return _json_or_none(response)


def api_put_data(url, status_code, data):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype,
        "Grpc-Metadata-Authorization": "Bearer test",
    }
    response = api_client.put(url, headers=headers, json=data)
    assert response.status_code == status_code, (
        url + " " + str(response.status_code)
    )
    return _json_or_none(response)
