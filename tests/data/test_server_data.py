import logging
import json
from node_agent.data.server_data import (
    get_server_ssh_map,
    server_ssh_data_create_full,
)
from tests.utils.user_util import user_util_get_test_organization

logger = logging.getLogger(__name__)


def test_server_data_ssh(fastapi_app):

    organization = user_util_get_test_organization(random=True)[2]
    organization_id = organization["id"]
    assert organization_id is not None
    ret1 = server_ssh_data_create_full(
        server_name="test_server",
        organization_id=organization_id,
        server_ip="127.0.0.1",
        cloud="test_cloud",
        cloud_name="Test Cloud",
        host_name="test_host",
        host_description="Test Host Description",
        port="22",
        port_description="Test Port Description",
        ssh_user_name="test_user",
        ssh_description="Test SSH Description",
    )
    assert ret1 is not None
    assert "server" in ret1
    assert "server_host" in ret1
    assert "server_port" in ret1
    assert "server_ssh" in ret1
    assert ret1["server"]["name"] == "test_server"
    ret2 = server_ssh_data_create_full(
        server_name="test_server_2",
        organization_id=organization_id,
        server_ip="127.0.0.2",
        cloud="test_cloud_2",
        cloud_name="Test Cloud 2",
        host_name="test_host_2",
        host_description="Test Host Description 2",
        port="2222",
        port_description="Test Port Description 2",
        ssh_user_name="test_user_2",
        ssh_description="Test SSH Description 2",
    )
    assert ret2 is not None
    assert "server" in ret2
    assert "server_host" in ret2
    assert "server_port" in ret2
    assert "server_ssh" in ret2
    assert ret2["server"]["name"] == "test_server_2"

    ssh_map = get_server_ssh_map(organization_id)
    logger.info(json.dumps(ssh_map, indent=2, default=str))
