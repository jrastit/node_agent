import logging

from tests.utils.api_util import (
    api_put_data,
    api_simple_get,
    api_simple_delete,
)
from tests.utils.user_util import (
    user_util_get_test_organization,
    user_util_get_test_user,
)

logger = logging.getLogger(__name__)


def test_api_server_post_error(fastapi_app):
    ret = api_put_data("/api/server", 422, {"error": False})
    assert ret is not None
    assert "detail" in ret

    ret = api_put_data(
        "/api/server",
        422,
        {
            "name": "api_test_server_missing_org",
            "ip": "127.0.0.1",
        },
    )
    assert ret is not None
    assert "detail" in ret


def test_api_server(fastapi_app):
    _, _, organization = user_util_get_test_organization()
    server_handler = api_put_data(
        "/api/server",
        200,
        {
            "name": "api_test_server",
            "ip": "127.0.0.1",
            "organization_id": organization["id"],
        },
    )
    assert "Server" in server_handler
    server = server_handler["Server"]
    assert "id" in server
    server_id = server["id"]
    assert "ip" in server
    assert server["ip"] == "127.0.0.1"
    server_handler = api_put_data(
        "/api/server",
        200,
        {
            "id": server_id,
            "name": "api_test_server",
            "ip": "127.0.0.2",
        },
    )
    assert "Server" in server_handler
    server = server_handler["Server"]
    assert "id" in server
    assert server["id"] == server_id
    assert "ip" in server
    assert server["ip"] == "127.0.0.2"

    server_list_handler = api_simple_get("/api/server", 200)
    assert "Server" in server_list_handler
    server_list = server_list_handler["Server"]
    found = False
    for _server in server_list:
        logger.info("Server: %s", _server)
        if _server["id"] == server_id:
            assert "ip" in _server
            assert _server["ip"] == "127.0.0.2"
            found = True
    assert found is True

    ret = api_simple_delete("/api/server/" + str(server_id), 200)
    assert "Status" in ret
    assert ret["Status"] == "success"

    server_list_handler = api_simple_get("/api/server", 200)
    assert "Server" in server_list_handler
    server_list = server_list_handler["Server"]
    found = False
    for _server in server_list:
        if _server["id"] == server_id:
            assert "ip" in _server
            assert _server["ip"] == "127.0.0.2"
            found = True
    assert found is False


def test_api_server_endpoint(fastapi_app):
    _, _, organization = user_util_get_test_organization()
    server_handler = api_put_data(
        "/api/server",
        200,
        {
            "name": "api_test_server",
            "ip": "127.0.0.1",
            "organization_id": organization["id"],
        },
    )
    assert "Server" in server_handler
    server = server_handler["Server"]
    assert "id" in server
    server_id = server["id"]

    entrypoint_handler = api_put_data(
        "/api/server/entrypoint",
        200,
        {
            "name": "api_test_entrypoint",
            "path": "/oasis",
            "user": "oasis",
            "error": "error",
            "server_id": server_id,
        },
    )
    assert "Entrypoint" in entrypoint_handler
    entrypoint = entrypoint_handler["Entrypoint"]
    assert "id" in entrypoint


def test_api_server_host_ip_ssh(fastapi_app):
    _, _, organization = user_util_get_test_organization()
    server_handler = api_put_data(
        "/api/server",
        200,
        {
            "name": "api_test_server_rel",
            "ip": "127.0.0.10",
            "organization_id": organization["id"],
        },
    )
    server = server_handler["Server"]
    server_id = server["id"]

    server_host_handler = api_put_data(
        "/api/server/host",
        200,
        {
            "name": "10.0.0.1",
            "description": "test host",
            "server_id": server_id,
        },
    )
    assert "ServerHost" in server_host_handler
    server_host = server_host_handler["ServerHost"]
    server_host_id = server_host["id"]
    assert server_host["name"] == "10.0.0.1"

    server_port_handler = api_put_data(
        "/api/server/port",
        200,
        {
            "port": "2200",
            "description": "test port",
            "server_host_id": server_host_id,
        },
    )
    assert "ServerPort" in server_port_handler
    server_port = server_port_handler["ServerPort"]
    server_port_id = server_port["id"]
    assert server_port["port"] == "2200"

    server_ssh_handler = api_put_data(
        "/api/server/ssh",
        200,
        {
            "user_name": "ubuntu",
            "description": "test ssh",
            "server_port_id": server_port_id,
        },
    )
    assert "ServerSSH" in server_ssh_handler
    server_ssh = server_ssh_handler["ServerSSH"]
    server_ssh_id = server_ssh["id"]
    assert server_ssh["user_name"] == "ubuntu"

    server_host_list_handler = api_simple_get("/api/server/host", 200)
    assert "ServerHost" in server_host_list_handler

    server_ip_list_handler = api_simple_get("/api/server/port", 200)
    assert "ServerPort" in server_ip_list_handler

    server_ssh_list_handler = api_simple_get("/api/server/ssh", 200)
    assert "ServerSSH" in server_ssh_list_handler

    ret = api_simple_delete(f"/api/server/ssh/{server_ssh_id}", 200)
    assert ret["Status"] == "success"

    ret = api_simple_delete(f"/api/server/port/{server_port_id}", 200)
    assert ret["Status"] == "success"

    ret = api_simple_delete(f"/api/server/host/{server_host_id}", 200)
    assert ret["Status"] == "success"

    ret = api_simple_delete(f"/api/server/{server_id}", 200)
    assert ret["Status"] == "success"
