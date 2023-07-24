from tests.utils.api_util import \
    api_put_data, \
    api_simple_get, \
    api_simple_delete


def test_api_server_post_error(app):
    ret = api_put_data(
        '/api/server',
        500,
        {
            "error": False
        }
    )
    assert ret is None


def test_api_server(app):
    server_handler = api_put_data(
        '/api/server',
        200,
        {
            "name": "api_test_server",
            "ip": "127.0.0.1",
        }
    )
    assert 'Server' in server_handler
    server = server_handler['Server']
    assert 'id' in server
    server_id = server['id']
    assert 'ip' in server
    assert server['ip'] == '127.0.0.1'
    server_handler = api_put_data(
        '/api/server',
        200,
        {
            "id": server_id,
            "name": "api_test_server",
            "ip": "127.0.0.2",
        }
    )
    assert 'Server' in server_handler
    server = server_handler['Server']
    assert 'id' in server
    assert server['id'] == server_id
    assert 'ip' in server
    assert server['ip'] == '127.0.0.2'

    server_list_handler = api_simple_get(
        '/api/server',
        200
    )
    assert 'Server' in server_list_handler
    server_list = server_list_handler['Server']
    found = False
    for _server in server_list:
        if _server['id'] == server_id:
            assert 'ip' in _server
            assert _server['ip'] == '127.0.0.2'
            found = True
    assert found is True

    ret = api_simple_delete(
        '/api/server/' + str(server_id),
        200
    )
    assert 'Status' in ret
    assert ret['Status'] == 'success'

    server_list_handler = api_simple_get(
        '/api/server',
        200
    )
    assert 'Server' in server_list_handler
    server_list = server_list_handler['Server']
    found = False
    for _server in server_list:
        if _server['id'] == server_id:
            assert 'ip' in _server
            assert _server['ip'] == '127.0.0.2'
            found = True
    assert found is False


def test_api_server_endpoint(app):
    server_handler = api_put_data(
        '/api/server',
        200,
        {
            "name": "api_test_server",
            "ip": "127.0.0.1",
        }
    )
    assert 'Server' in server_handler
    server = server_handler['Server']
    assert 'id' in server
    server_id = server['id']

    entrypoint_handler = api_put_data(
        '/api/server/entrypoint',
        200,
        {
            "name": "api_test_entrypoint",
            "path": "/oasis",
            "user": "oasis",
            "error": "error",
            "server_id": server_id,
        }
    )
    assert 'Entrypoint' in entrypoint_handler
    entrypoint = entrypoint_handler['Entrypoint']
    assert 'id' in entrypoint



