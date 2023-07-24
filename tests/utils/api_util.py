from tests.conftest import init_app

flask_app = init_app()


def api_get(url, status_code, params):
    with flask_app.test_client() as test_client:
        response = test_client.get(
            url,
            headers={"Grpc-Metadata-Authorization": "Bearer test"},
            query_string=params
        )
        assert response.status_code == status_code, \
            'status code : ' + str(response.status_code) + \
            ' ' + str(response.get_data())
        return response.get_json()


def api_simple_get(url, status_code):
    with flask_app.test_client() as test_client:
        response = test_client.get(
            url,
            headers={"Grpc-Metadata-Authorization": "Bearer test"}
        )
        assert response.status_code == status_code, \
            'status code : ' + str(response.status_code) + \
            ' ' + str(response.get_json())
        return response.get_json()


def api_simple_delete(url, status_code):
    with flask_app.test_client() as test_client:
        response = test_client.delete(
            url,
            headers={"Grpc-Metadata-Authorization": "Bearer test"}
        )
        assert response.status_code == status_code, \
            'status code : ' + str(response.status_code) + \
            ' ' + str(response.get_json())
        return response.get_json()


def api_simple_post(url, status_code):
    with flask_app.test_client() as test_client:
        response = test_client.post(
            url,
            headers={"Grpc-Metadata-Authorization": "Bearer test"}
        )
        assert response.status_code == status_code
        return response.get_json()


def api_post_data(url, status_code, data):
    with flask_app.test_client() as test_client:
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            "Grpc-Metadata-Authorization": "Bearer test"
        }
        response = test_client.post(url, headers=headers, json=data)
        assert response.status_code == status_code
        return response.get_json()


def api_put_data(url, status_code, data):
    with flask_app.test_client() as test_client:
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            "Grpc-Metadata-Authorization": "Bearer test"
        }
        response = test_client.put(url, headers=headers, json=data)
        assert response.status_code == status_code, \
            url + " " + str(response.status_code)
        return response.get_json()
